#ifndef DASHBOARD_UI_H
#define DASHBOARD_UI_H

#include "dashboard_model.h"
#include "lvgl_display.h"

#if HAVE_LVGL
#include <lvgl.h>
#endif

#include <string>

class DashboardUI {
public:
    DashboardUI();
    ~DashboardUI();

    void SetupIdleUI(lv_obj_t *parent, int screen_width, int screen_height);
    void ShowIdleCard(const DashboardInfo &info);
    void HideIdleCard();

    bool IsInitialized() const { return container_ != nullptr; }

private:
    lv_obj_t *container_;
    int screen_width_;
    int screen_height_;

    /* Title */
    lv_obj_t *label_title_;

    /* Sensor */
    lv_obj_t *label_temperature_;
    lv_obj_t *label_humidity_;

    /* Relay */
    lv_obj_t *label_relay_;
};

#endif // DASHBOARD_UI_H