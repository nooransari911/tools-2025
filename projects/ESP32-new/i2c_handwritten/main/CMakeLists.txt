idf_component_register(SRCS "i2c_handwritten.c"
                       INCLUDE_DIRS "."
                       PRIV_REQUIRES esp_driver_i2c
                       PRIV_REQUIRES esp_driver_gpio
                     )
