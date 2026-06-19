#include "tensorflow/compiler/xla/service/custom_call_status.h"

#include <optional>
#include <string>

struct XlaCustomCallStatus_ {
  std::optional<std::string> message;
};

extern "C" {

void XlaCustomCallStatusSetSuccess(XlaCustomCallStatus* status) {
  if (status) {
    reinterpret_cast<XlaCustomCallStatus_*>(status)->message = std::nullopt;
  }
}

void XlaCustomCallStatusSetFailure(
    XlaCustomCallStatus* status, const char* message, size_t message_len) {
  if (status && message) {
    reinterpret_cast<XlaCustomCallStatus_*>(status)->message =
        std::string(message, message_len);
  }
}

}  // extern "C"

