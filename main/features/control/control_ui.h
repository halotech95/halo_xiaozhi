#ifndef CONTROL_UI_H
#define CONTROL_UI_H

#include "control_model.h"
#include "lvgl_display.h"

#if HAVE_LVGL
#include <lvgl.h>
#endif

#include <vector>

class ControlUI {
public:
    ControlUI();
    ~ControlUI();

    void SetupUI(lv_obj_t* parent,
                 int screen_width,
                 int screen_height);

    void Update(const ControlInfo& info);

    void Show();
    void Hide();

    bool IsInitialized() const { return container_ != nullptr; }

private:
    lv_obj_t* container_;

    int screen_width_;
    int screen_height_;

    lv_obj_t* title_;

    std::vector<lv_obj_t*> button_list_;
    std::vector<lv_obj_t*> label_list_;
};

#endif