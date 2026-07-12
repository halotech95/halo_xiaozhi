#include "control_ui.h"

LV_FONT_DECLARE(lv_font_montserrat_20);
LV_FONT_DECLARE(lv_font_montserrat_28);

ControlUI::ControlUI()
    : container_(nullptr),
      screen_width_(0),
      screen_height_(0),
      title_(nullptr) {
}

ControlUI::~ControlUI() {
}

void ControlUI::SetupUI(lv_obj_t* parent, int screen_width, int screen_height)
{
    screen_width_ = screen_width;
    screen_height_ = screen_height;

    container_ = lv_obj_create(parent);
    lv_obj_remove_style_all(container_);

    lv_obj_set_size(container_, screen_width_, screen_height_);
    lv_obj_set_style_bg_color(container_, lv_color_black(), 0);
    lv_obj_set_style_bg_opa(container_, LV_OPA_COVER, 0);

    lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);

    //---------------------------------------
    // Title
    //---------------------------------------

    title_ = lv_label_create(container_);

    lv_obj_set_style_text_font(title_, &lv_font_montserrat_20, 0);
    lv_obj_set_style_text_color(title_, lv_color_white(), 0);

    lv_label_set_text(title_, "SMART HOME");

    lv_obj_align(title_, LV_ALIGN_TOP_MID, 0, 10);
}

void ControlUI::Update(const ControlInfo& info)
{
    for (auto obj : button_list_) {
        lv_obj_del(obj);
    }

    button_list_.clear();
    label_list_.clear();

    int y = 50;

    for (const auto& dev : info.devices) {

        lv_obj_t* btn = lv_btn_create(container_);

        lv_obj_set_size(btn, screen_width_ - 20, 42);
        lv_obj_align(btn, LV_ALIGN_TOP_MID, 0, y);

        if (!dev.online) {
            lv_obj_set_style_bg_color(btn,
                                      lv_palette_main(LV_PALETTE_GREY),
                                      0);
        } else if (dev.state) {
            lv_obj_set_style_bg_color(btn,
                                      lv_palette_main(LV_PALETTE_GREEN),
                                      0);
        } else {
            lv_obj_set_style_bg_color(btn,
                                      lv_palette_main(LV_PALETTE_RED),
                                      0);
        }

        lv_obj_t* label = lv_label_create(btn);

        char text[64];

        snprintf(text,
                 sizeof(text),
                 "%s   %s",
                 dev.name.c_str(),
                 dev.state ? "ON" : "OFF");

        lv_label_set_text(label, text);

        lv_obj_center(label);

        button_list_.push_back(btn);
        label_list_.push_back(label);

        y += 50;
    }
}

void ControlUI::Show()
{
    if (container_) {
        lv_obj_clear_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}

void ControlUI::Hide()
{
    if (container_) {
        lv_obj_add_flag(container_, LV_OBJ_FLAG_HIDDEN);
    }
}