#include <iostream>
#include <librealsense2/rs.hpp>

auto main(int /*argc*/, char * /*argv*/[]) -> int {
  try {
    auto ctx = rs2::context();
    bool devices_found = false;
    for (auto &&dev : ctx.query_devices()) {
      const auto *name = dev.get_info(RS2_CAMERA_INFO_NAME);
      const auto *serno = dev.get_info(RS2_CAMERA_INFO_SERIAL_NUMBER);
      std::cout << "Found " << name << " S/N: " << serno << "\n";
      devices_found = true;
      dev.hardware_reset();
    }
    if (!devices_found) {
      std::cerr << "No devices found\n";
      return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
  } catch (const rs2::error &e) {
    std::cerr << "RealSense error calling " << e.get_failed_function() << "("
              << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
  } catch (const std::exception &e) {
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
  }
}
