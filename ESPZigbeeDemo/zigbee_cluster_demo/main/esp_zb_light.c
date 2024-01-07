/*
 * SPDX-FileCopyrightText: 2021-2023 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: LicenseRef-Included
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form, except as embedded into a Espressif Systems
 *    integrated circuit in a product or a software update for such product,
 *    must reproduce the above copyright notice, this list of conditions and
 *    the following disclaimer in the documentation and/or other materials
 *    provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its contributors
 *    may be used to endorse or promote products derived from this software without
 *    specific prior written permission.
 *
 * 4. Any software provided in binary form under this license must not be reverse
 *    engineered, decompiled, modified and/or disassembled.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_check.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "ha/esp_zigbee_ha_standard.h"
#include "esp_zb_light.h"
#include "zboss_api.h"

#if !defined ZB_ED_ROLE
#error Define ZB_ED_ROLE in idf.py menuconfig to compile light (End Device) source code.
#endif

// The first byte of a string sent via zigbee must be its length - as a placeholder, use a space
char modelid[] = " ZigbeeDemo";
char manufname[] = " Dragon Curve Brewing";

static const char *TAG = "ESP_ZB_ON_OFF_LIGHT";
/********************* Define functions **************************/
static void bdb_start_top_level_commissioning_cb(uint8_t mode_mask)
{
    ESP_ERROR_CHECK(esp_zb_bdb_start_top_level_commissioning(mode_mask));
}

void esp_zb_app_signal_handler(esp_zb_app_signal_t *signal_struct)
{
    uint32_t *p_sg_p       = signal_struct->p_app_signal;
    esp_err_t err_status = signal_struct->esp_err_status;
    esp_zb_app_signal_type_t sig_type = *p_sg_p;
    switch (sig_type) {
    case ESP_ZB_ZDO_SIGNAL_SKIP_STARTUP:
        ESP_LOGI(TAG, "Zigbee stack initialized");
        esp_zb_bdb_start_top_level_commissioning(ESP_ZB_BDB_MODE_INITIALIZATION);
        break;
    case ESP_ZB_BDB_SIGNAL_DEVICE_FIRST_START:
    case ESP_ZB_BDB_SIGNAL_DEVICE_REBOOT:
        if (err_status == ESP_OK) {
            ESP_LOGI(TAG, "Start network steering");
            esp_zb_bdb_start_top_level_commissioning(ESP_ZB_BDB_MODE_NETWORK_STEERING);
        } else {
            /* commissioning failed */
            ESP_LOGW(TAG, "Failed to initialize Zigbee stack (status: %s)", esp_err_to_name(err_status));
        }
        break;
    case ESP_ZB_BDB_SIGNAL_STEERING:
        if (err_status == ESP_OK) {
            esp_zb_ieee_addr_t extended_pan_id;
            esp_zb_get_extended_pan_id(extended_pan_id);
            ESP_LOGI(TAG, "Joined network successfully (Extended PAN ID: %02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x, PAN ID: 0x%04hx, Channel:%d)",
                     extended_pan_id[7], extended_pan_id[6], extended_pan_id[5], extended_pan_id[4],
                     extended_pan_id[3], extended_pan_id[2], extended_pan_id[1], extended_pan_id[0],
                     esp_zb_get_pan_id(), esp_zb_get_current_channel());
        } else {
            ESP_LOGI(TAG, "Network steering was not successful (status: %s)", esp_err_to_name(err_status));
            esp_zb_scheduler_alarm((esp_zb_callback_t)bdb_start_top_level_commissioning_cb, ESP_ZB_BDB_MODE_NETWORK_STEERING, 1000);
        }
        break;
    default:
        ESP_LOGI(TAG, "ZDO signal: %s (0x%x), status: %s", esp_zb_zdo_signal_to_string(sig_type), sig_type,
                 esp_err_to_name(err_status));
        break;
    }
}

static esp_err_t zb_attribute_handler(const esp_zb_zcl_set_attr_value_message_t *message)
{
    esp_err_t ret = ESP_OK;
    bool light_state = 0;

    ESP_RETURN_ON_FALSE(message, ESP_FAIL, TAG, "Empty message");
    ESP_RETURN_ON_FALSE(message->info.status == ESP_ZB_ZCL_STATUS_SUCCESS, ESP_ERR_INVALID_ARG, TAG,
                        "Received message: error status(%d)", message->info.status);
    ESP_LOGI(TAG, "Received message: endpoint(%d), cluster(0x%x), attribute(0x%x), data size(%d), data(%d)",
             message->info.dst_endpoint, message->info.cluster, message->attribute.id, message->attribute.data.size, *(bool *)message->attribute.data.value);
    if (message->info.dst_endpoint == HA_ESP_LIGHT_ENDPOINT) {
        if (message->info.cluster == ESP_ZB_ZCL_CLUSTER_ID_ON_OFF) {
            if (message->attribute.id == ESP_ZB_ZCL_ATTR_ON_OFF_ON_OFF_ID &&
                message->attribute.data.type == ESP_ZB_ZCL_ATTR_TYPE_BOOL) {
                light_state = message->attribute.data.value ? *(bool *)message->attribute.data.value : light_state;
                ESP_LOGI(TAG, "Light set to %s", light_state ? "On" : "Off");
                light_driver_set_power(light_state);
            }
        } else if (message->info.cluster == ESP_ZB_ZCL_CLUSTER_ID_COLOR_CONTROL) {
            ESP_LOGI(TAG, "Color control command");
            ESP_LOGI(TAG, "Attribute ID: %d", message->attribute.id);
            uint16_t color_temp = *(uint16_t *) message->attribute.data.value;
            ESP_LOGI(TAG, "Color temp set to %d", color_temp);
        } else if (message->info.cluster == ESP_ZB_ZCL_CLUSTER_ID_ANALOG_OUTPUT) {
            float analog_output_new_value = *(float *) message->attribute.data.value;
            ESP_LOGI(TAG, "Analog output set to %f", analog_output_new_value);
        } else if (message->info.cluster == ESP_ZB_ZCL_CLUSTER_ID_MULTI_VALUE) {
            uint16_t multistate_value_new_value = *(uint16_t *) message->attribute.data.value;
            ESP_LOGI(TAG, "Multistate value set to %d", multistate_value_new_value);
        }
    }
    return ret;
}

static esp_err_t zb_action_handler(esp_zb_core_action_callback_id_t callback_id, const void *message)
{
    esp_err_t ret = ESP_OK;
    ESP_LOGI(TAG, "Action Handler Run");
    switch (callback_id) {
    case ESP_ZB_CORE_SET_ATTR_VALUE_CB_ID:
        ret = zb_attribute_handler((esp_zb_zcl_set_attr_value_message_t *)message);
        break;
    default:
        ESP_LOGW(TAG, "Receive Zigbee action(0x%x) callback", callback_id);
        break;
    }
    return ret;
}

static void esp_zb_task(void *pvParameters)
{
    /* initialize Zigbee stack with Zigbee end-device config */
    esp_zb_cfg_t zb_nwk_cfg = ESP_ZB_ZED_CONFIG();
    esp_zb_init(&zb_nwk_cfg);
    esp_zb_set_primary_network_channel_set(ESP_ZB_PRIMARY_CHANNEL_MASK);

    /* create cluster list for this endpoint */
    esp_zb_cluster_list_t *esp_zb_cluster_list = esp_zb_zcl_cluster_list_create();

    /* Basic cluster (Used to provide zigbee2mqtt with the custom model and manufacturer to it knows how to read the data) */
    // The first byte of a string sent via zigbee must be its length
    modelid[0] = strlen(modelid);
    manufname[0] = strlen(manufname);
    esp_zb_attribute_list_t *esp_zb_basic_cluster = esp_zb_zcl_attr_list_create(ESP_ZB_ZCL_CLUSTER_ID_BASIC);
    esp_zb_basic_cluster_add_attr(esp_zb_basic_cluster, ESP_ZB_ZCL_ATTR_BASIC_MODEL_IDENTIFIER_ID, &modelid[0]);
    esp_zb_basic_cluster_add_attr(esp_zb_basic_cluster, ESP_ZB_ZCL_ATTR_BASIC_MANUFACTURER_NAME_ID, &manufname[0]);
    esp_zb_cluster_list_add_basic_cluster(esp_zb_cluster_list, esp_zb_basic_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE);
    
    /* On-off cluster (used for alarm and two way valve control)*/
    esp_zb_on_off_cluster_cfg_t on_off_cfg;
    on_off_cfg.on_off = ESP_ZB_ZCL_ON_OFF_ON_OFF_DEFAULT_VALUE;
    esp_zb_attribute_list_t *esp_zb_on_off_cluster = esp_zb_on_off_cluster_create(&on_off_cfg);
    esp_zb_cluster_list_add_on_off_cluster(esp_zb_cluster_list, esp_zb_on_off_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE);

    // Color control cluster (Not used, but was a good testing ground)
    uint16_t color_attr = ESP_ZB_ZCL_COLOR_CONTROL_COLOR_TEMPERATURE_DEF_VALUE;
    uint16_t min_temp = ESP_ZB_ZCL_COLOR_CONTROL_COLOR_TEMP_PHYSICAL_MIN_MIREDS_DEFAULT_VALUE;
    uint16_t max_temp = ESP_ZB_ZCL_COLOR_CONTROL_COLOR_TEMP_PHYSICAL_MAX_MIREDS_DEFAULT_VALUE;
    uint8_t color_mode = 0x0002;  // ColorTemperatureMireds
    uint8_t color_capabilities = 0x0010; // Color temperature supported

    esp_zb_attribute_list_t *esp_zb_color_cluster = esp_zb_zcl_attr_list_create(ESP_ZB_ZCL_CLUSTER_ID_COLOR_CONTROL);
    esp_zb_color_control_cluster_add_attr(esp_zb_color_cluster, ESP_ZB_ZCL_ATTR_COLOR_CONTROL_COLOR_MODE_ID, &color_mode);
    esp_zb_color_control_cluster_add_attr(esp_zb_color_cluster, ESP_ZB_ZCL_ATTR_COLOR_CONTROL_COLOR_CAPABILITIES_ID, &color_capabilities);
    esp_zb_color_control_cluster_add_attr(esp_zb_color_cluster, ESP_ZB_ZCL_ATTR_COLOR_CONTROL_COLOR_TEMPERATURE_ID, &color_attr);
    esp_zb_color_control_cluster_add_attr(esp_zb_color_cluster, ESP_ZB_ZCL_ATTR_COLOR_CONTROL_COLOR_TEMP_PHYSICAL_MIN_MIREDS_ID, &min_temp);
    esp_zb_color_control_cluster_add_attr(esp_zb_color_cluster, ESP_ZB_ZCL_ATTR_COLOR_CONTROL_COLOR_TEMP_PHYSICAL_MAX_MIREDS_ID, &max_temp);
    esp_zb_cluster_list_add_color_control_cluster(esp_zb_cluster_list, esp_zb_color_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE);

    // Analog output cluster (Used for control of the heating element)
    esp_zb_analog_output_cluster_cfg_t analog_output_cfg;
    analog_output_cfg.out_of_service = 0;
    analog_output_cfg.present_value = 0;
    esp_zb_attribute_list_t *esp_zb_analog_output_cluster = esp_zb_analog_output_cluster_create(&analog_output_cfg);
    esp_zb_cluster_list_add_analog_output_cluster(esp_zb_cluster_list, esp_zb_analog_output_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE);

    // Analog input cluster (Currently used for flow sensor - should be replaced with flow measurement when ESP supports it)
    esp_zb_analog_input_cluster_cfg_t analog_input_cfg;
    analog_input_cfg.out_of_service = 0;
    analog_input_cfg.present_value = 0;
    analog_input_cfg.status_flags = ESP_ZB_ZCL_ANALOG_INPUT_STATUS_FLAG_DEFAULT_VALUE;
    esp_zb_attribute_list_t *esp_zb_analog_input_cluster = esp_zb_analog_input_cluster_create(&analog_input_cfg);
    esp_zb_cluster_list_add_analog_input_cluster(esp_zb_cluster_list, esp_zb_analog_input_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE);

    // Multistate value cluster (Used for three way valves. It is not clear why multistate output is not implemented, or how it is different than multistate output, so this is what I am using)
    esp_zb_multistate_value_cluster_cfg_t multistate_value_cfg;
    multistate_value_cfg.out_of_service = 0;
    multistate_value_cfg.present_value = 0;
    multistate_value_cfg.status_flags = ESP_ZB_ZCL_MULTI_VALUE_STATUS_FLAGS_DEFAULT_VALUE;
    multistate_value_cfg.number_of_states = 3;
    esp_zb_attribute_list_t *esp_zb_multistate_value_cluster = esp_zb_multistate_value_cluster_create(&multistate_value_cfg);
    esp_zb_cluster_list_add_multistate_value_cluster(esp_zb_cluster_list, esp_zb_multistate_value_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE);
    

    // Pressure measurement cluster (used for volume sensors)
    esp_zb_pressure_meas_cluster_cfg_t pressure_meas_cfg;
    pressure_meas_cfg.max_value = 1000;
    pressure_meas_cfg.min_value = 0;
    pressure_meas_cfg.measured_value = 0;
    esp_zb_attribute_list_t *esp_zb_pressure_meas_cluster = esp_zb_pressure_meas_cluster_create(&pressure_meas_cfg);
    esp_zb_cluster_list_add_pressure_meas_cluster(esp_zb_cluster_list, esp_zb_pressure_meas_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE);

    // Temperature measurement cluster (used for temperature sensors)
    esp_zb_temperature_meas_cluster_cfg_t temperature_meas_cfg;
    temperature_meas_cfg.max_value = 1000;
    temperature_meas_cfg.min_value = 0;
    temperature_meas_cfg.measured_value = 0;
    esp_zb_attribute_list_t *esp_zb_temperature_meas_cluster = esp_zb_temperature_meas_cluster_create(&temperature_meas_cfg);
    esp_zb_cluster_list_add_temperature_meas_cluster(esp_zb_cluster_list, esp_zb_temperature_meas_cluster, ESP_ZB_ZCL_CLUSTER_SERVER_ROLE);
    
    /* add created endpoint (cluster_list) to endpoint list */
    esp_zb_ep_list_t *esp_zb_ep_list = esp_zb_ep_list_create();
    esp_zb_ep_list_add_ep(esp_zb_ep_list, esp_zb_cluster_list, HA_ESP_LIGHT_ENDPOINT, ESP_ZB_AF_HA_PROFILE_ID, ESP_ZB_HA_ON_OFF_OUTPUT_DEVICE_ID);
    esp_zb_device_register(esp_zb_ep_list);
    esp_zb_core_action_handler_register(zb_action_handler);
    ESP_ERROR_CHECK(esp_zb_start(false));
    esp_zb_main_loop_iteration();
}

void app_main(void)
{
    esp_zb_platform_config_t config = {
        .radio_config = ESP_ZB_DEFAULT_RADIO_CONFIG(),
        .host_config = ESP_ZB_DEFAULT_HOST_CONFIG(),
    };
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_zb_platform_config(&config));
    light_driver_init(LIGHT_DEFAULT_OFF);
    xTaskCreate(esp_zb_task, "Zigbee_main", 4096, NULL, 5, NULL);
}
