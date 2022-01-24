from pasco import CodeNodeDevice, Icons
import time


def main():
    code_node = CodeNodeDevice()
    code_node.connect_by_id('481-782')

    code_node.show_image_in_array(Icons().smile)
    time.sleep(1)
    code_node.show_image_in_array(Icons().sad)
    time.sleep(1)
    code_node.show_image_in_array(Icons().surprise)
    time.sleep(1)
    code_node.show_image_in_array(Icons().arrow_top)
    time.sleep(1)
    code_node.show_image_in_array(Icons().arrow_top_right)
    time.sleep(1)
    code_node.show_image_in_array(Icons().arrow_right)
    time.sleep(1)
    code_node.show_image_in_array(Icons().arrow_bottom_right)
    time.sleep(1)
    code_node.show_image_in_array(Icons().arrow_bottom)
    time.sleep(1)
    code_node.show_image_in_array(Icons().arrow_bottom_left)
    time.sleep(1)
    code_node.show_image_in_array(Icons().arrow_left)
    time.sleep(1)
    code_node.show_image_in_array(Icons().arrow_top_left)
    time.sleep(1)
    code_node.show_image_in_array(Icons().heart)
    time.sleep(1)
    code_node.show_image_in_array(Icons().heart_sm)
    time.sleep(1)
    code_node.show_image_in_array(Icons().alien)
    time.sleep(1)

    code_node.reset()


if __name__ == "__main__":
    main()
