#include "dashboard_ui.h"

LV_FONT_DECLARE(lv_font_montserrat_20);
LV_FONT_DECLARE(lv_font_montserrat_28);

DashboardUI::DashboardUI()
    : container_(nullptr),
      screen_width_(0),
      screen_height_(0),
      label_title_(nullptr),
      label_temperature_(nullptr),
      label_humidity_(nullptr),
      label_relay_(nullptr)
{
}

DashboardUI::~DashboardUI()
{
    if (container_) {
        lv_obj_del(container_);
        container_ = nullptr;
    }
}

void DashboardUI::SetupIdleUI(lv_obj_t *parent,
                              int screen_width,
                              int screen_height)
{
    screen_width_ = screen_width;
    screen_height_ = screen_height;

    container_ = lv_obj_create(parent);
    lv_obj_set_size(container_, screen_width_, screen_height_);
    lv_obj_center(container_);

    lv_obj_set_style_radius(container_, 0, 0);
    lv_obj_set_style_border_width(container_, 0, 0);
    lv_obj_set_style_bg_color(container_, lv_color_black(), 0);

    lv_obj_clear_flag(container_, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);

    lv_obj_set_flex_flow(container_, LV_FLEX_FLOW_COLUMN);
    lv_obj_set_flex_align(container_,
                          LV_FLEX_ALIGN_CENTER,
                          LV_FLEX_ALIGN_CENTER,
                          LV_FLEX_ALIGN_CENTER);

    lv_obj_set_style_pad_row(container_, 20, 0);

    /* Title */
    label_title_ = lv_label_create(container_);
    lv_obj_set_style_text_font(label_title_, &lv_font_montserrat_28, 0);
    lv_label_set_text(label_title_, "SMART HOME");

    /* Temperature */
    label_temperature_ = lv_label_create(container_);
    lv_obj_set_style_text_font(label_temperature_, &lv_font_montserrat_20, 0);
    lv_label_set_text(label_temperature_, "Temperature : --.- C");

    /* Humidity */
    label_humidity_ = lv_label_create(container_);
    lv_obj_set_style_text_font(label_humidity_, &lv_font_montserrat_20, 0);
    lv_label_set_text(label_humidity_, "Humidity    : --.- %");

    /* Relay */
    label_relay_ = lv_label_create(container_);
    lv_obj_set_style_text_font(label_relay_, &lv_font_montserrat_20, 0);
    lv_label_set_text(label_relay_, "Relay       : OFF");
}

void DashboardUI::ShowIdleCard(const DashboardInfo &info)
{
    if (!container_)
        return;

    lv_label_set_text_fmt(label_temperature_,
                          "Temperature : %.1f C",
                          info.temperature);

    lv_label_set_text_fmt(label_humidity_,
                          "Humidity    : %.1f %%",
                          info.humidity);

    lv_label_set_text_fmt(label_relay_,
                          "Relay       : %s",
                          info.relay ? "ON" : "OFF");

    lv_obj_remove_flag(container_, LV_OBJ_FLAG_HIDDEN);
}

void DashboardUI::HideIdleCard()
{
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}