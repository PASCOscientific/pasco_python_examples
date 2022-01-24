from pasco import CodeNodeDevice, Icons, PASCOBLEDevice


def main():
    code_node = CodeNodeDevice('//code.Node')
    force_sensor = PASCOBLEDevice('Force')

    code_node.reset()
    light_on = False

    while code_node.read_data('Button1') == 0:
        if force_sensor.read_data('Force') > 10:
            if light_on == False:
                code_node.set_rgb_led(100,100,100)
                code_node.show_image_in_array(Icons().smile)
                light_on = True
            else:
                code_node.reset()
                light_on = False

            while force_sensor.read_data('Force') > 10:
                pass


if __name__ == "__main__":
    main()
