class AddressSize:
    def __init__(self, address, size):
        self.address = address
        self.size = size

class ControlTableAX12A:
    def __init__(self):
        self.model_number = AddressSize(0, 2)
        self.firmware_version = AddressSize(2, 1)
        self.id = AddressSize(3, 1)
        self.baud_rate = AddressSize(4, 1)
        self.return_delay_time = AddressSize(5, 1)
        self.cw_angle_limit = AddressSize(6, 2)
        self.ccw_angle_limit = AddressSize(8, 2)
        self.temperature_limit = AddressSize(11, 1)
        self.min_voltage_limit = AddressSize(12, 1)
        self.max_voltage_limit = AddressSize(13, 1)
        self.max_torque = AddressSize(14, 2)
        self.status_return_level = AddressSize(16, 1)
        self.alarm_led = AddressSize(17, 1)
        self.shutdown = AddressSize(18, 1)
        self.torque_enable = AddressSize(24, 1)
        self.led = AddressSize(25, 1)
        self.cw_compliance_margin = AddressSize(26, 1)
        self.ccw_compliance_margin = AddressSize(27, 1)
        self.cw_compliance_slope = AddressSize(28, 1)
        self.ccw_compliance_slope = AddressSize(29, 1)
        self.goal_position = AddressSize(30, 2)
        self.moving_speed = AddressSize(32, 2)
        self.torque_limit = AddressSize(34, 2)
        self.present_position = AddressSize(36, 2)
        self.present_speed = AddressSize(38, 2)
        self.present_load = AddressSize(40, 2)
        self.present_voltage = AddressSize(42, 1)
        self.present_temperature = AddressSize(43, 1)
        self.registered = AddressSize(44, 1)
        self.moving = AddressSize(46, 1)
        self.lock = AddressSize(47, 1)
        self.punch = AddressSize(48, 2)



class mkDynamixel:
    supported_models = ["AX-12A"]
    def __init__(self, id, model, port_handler, packet_handler):
        if model not in self.supported_models:
            raise ValueError("Model " + str(model) + " is not supported")
        
        if id < 1 or id > 253:
            raise ValueError("ID " + str(id) + " is not valid")

        if port_handler is None:
            raise ValueError("PortHandler is not valid")
        
        if packet_handler is None:
            raise ValueError("PacketHandler is not valid")

        self.id = id
        self.model = model
        self.port_handler = port_handler
        self.packet_handler = packet_handler


        if self.model == "AX-12A":
            self.control_table = ControlTableAX12A()
        # TODO: Add other models
        else:
            raise ValueError("Model " + str(model) + " is not supported")



    def set_torque(self, onoff):
        result, error = self.packet_handler.write1ByteTxRx(self.port_handler, self.id, self.control_table.torque_enable.address, onoff)
        if result != 0:
            raise ValueError("Failed to set torque")
        return result, error


    def set_position(self, position):
        dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, self.id, self.control_table.goal_position.address, position)
        if dxl_comm_result != 0:
            print("%s" % self.packet_handler.getTxRxResult(dxl_comm_result))
            print("%s" % self.packet_handler.getRxPacketError(dxl_error))


    def get_position(self):
        dxl_present_position, dxl_comm_result, dxl_error = self.packet_handler.read2ByteTxRx(self.port_handler, self.id, self.control_table.present_position.address)
        if dxl_comm_result != 0:
            print("%s" % self.packet_handler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packet_handler.getRxPacketError(dxl_error))