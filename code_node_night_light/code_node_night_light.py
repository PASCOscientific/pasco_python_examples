from pasco.code_node_device import CodeNodeDevice


def main():
    code_node = CodeNodeDevice()
    code_node.connect_by_id('481-782')

    while code_node.read_data('Button1') == 0:
        if code_node.read_data('Brightness') < 2:
            code_node.set_rgb_led(100,100,100)
        else:
            code_node.set_rgb_led(0,0,0)

    code_node.disconnect()


if __name__ == "__main__":
    main()
