import cv2
from pyzbar.pyzbar import decode
from djitellopy import tello

mydrone =tello.Tello()
mydrone.connect()
mydrone.streamon()


# QRコードを読むためのカメラを初期化
#cap = cv2.VideoCapture(0)  # カメラデバイスの番号を指定


# Telloドローンが離陸したかどうかを示すフラグ
is_taken_off = False
#着陸フラグ
is_land_off=True


while True:
    
    #ret, frame = cap.read()
    frame =mydrone.get_frame_read().frame
    #if not ret:
    
     #   break
 
    # QRコードを読み取り
    decoded_objects = decode(frame)

    # 画面に表示するテキスト
    display_text = []

    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        print(f"QR Code Data: {data}")

        # QRコードデータをコンマで分割
        qr_data = data.split(',')

        # 各QRコマンドごとに画面情報を初期化
        display_text = []

        for qr_command in qr_data:
            # 各QRコマンドの形式は "コマンド=値" とする
            command, value = qr_command.split(':')

            if command == "takeoff":
                if value == "1" and not is_taken_off:
                    mydrone.takeoff()
                    is_taken_off = True
            elif command == "land":
                if value == "1" and is_taken_off and is_land_off:
                    mydrone.land()
                    is_land_off=False
            elif command == "left":
                if int(value) > 0 and is_taken_off:
                    mydrone.move_left(int(value))
            elif command == "right":
                if int(value) > 0 and is_taken_off:
                    mydrone.move_right(int(value))
            elif command == "up":
                if int(value) > 0 and is_taken_off:
                    mydrone.move_up(int(value))
            elif command == "down":
                if int(value) > 0 and is_taken_off:
                    mydrone.move_down(int(value))
            elif command == "rotate_clockwise":
                if int(value) > 0 and is_taken_off:
                    mydrone.rotate_clockwise(int(value))
            elif command == "flip":
                if value:
                    if value == "l":
                        mydrone.flip("l")
                    elif value == "r":
                        mydrone.flip("r")
                    elif value == "f":
                        mydrone.flip("f")
                    elif value == "b":
                        mydrone.flip("b")
            # 新しいコマンド情報を画面に表示
            display_text.append(f"{command}:{value}")

    # 画面にテキストを表示
    text_to_display = ", ".join(display_text)
    cv2.putText(frame, text_to_display, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 画面に映像を表示
    cv2.imshow('QR Code Detection', frame)
  
    # 'q' キーを押すとプログラムが終了
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    

mydrone.land()
mydrone.end()
frame.release()
cv2.destroyAllWindows()