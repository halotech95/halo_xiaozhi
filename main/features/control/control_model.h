#ifndef CONTROL_MODEL_H
#define CONTROL_MODEL_H

#include <string>
#include <vector>

struct DeviceItem {
    std::string id;
    std::string name;
    bool state;
    bool online;
};

struct ControlInfo {
    std::vector<DeviceItem> devices;
};

#endif