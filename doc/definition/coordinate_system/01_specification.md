#### Coordinate System

##### Robot

座標系の表現にばらつきがあることを認識することが不可欠です。

![elimination_GH-UXTmakAAawXH.jpg](/assets/HumaroidCommonInterface/elimination_GH-UXTmakAAawXH.jpg "[TODO]画像差し替え/ パーツリスト")
[link](https://www.linkedin.com/posts/vanessaloiola_wednesdayinfo-robot-robot-activity-7171038547213279233-quC2)

座標系は動作する空間内の位置を定義し、X/Y/Z （またはロール/ピッチ/ヨー）の 3 つの軸と回転軸で構成されます。ロボットの中心または指定された基準点を原点に交差します。

![CoordinateSystem.png](/assets/HumaroidCommonInterface/CoordinateSystem.png "CoordinateSystem"){width="50%"}


この基準が整っていないと想定の動きとは逆の動きをすることがあります。

![elimination_picture_pc_f138e4902aa7db782e6629f68b9fbf2f.png](/assets/HumaroidCommonInterface/elimination_picture_pc_f138e4902aa7db782e6629f68b9fbf2f.png "[TODO]画像差し替え/ パーツリスト")



##### Room

筐体座標とは別にSLAMなどを使うようにするため、ロボット間で位置情報を共有するために、部屋の原点を定義する必要があります。

!!! todo
    SLAMなどを使う場合の部屋の原点はどうするか？
    * 部屋に段差がある家（ライブハウスなど）の場合、どうするか？
    * 未知の部屋に入ることを考えると、外へ出れる個所を「原点」になるのか？
    * 扉の種類によって、どこを原点にするか

    ![room_starting_point.png](/assets/HumaroidCommonInterface/room_starting_point.png "[TODO]画像差し替え/ パーツリスト")

    * 懸念
      * 部屋の角を原点とした場合、真四角でない部屋の場合にどこを原点にするかでもめる
      * 部屋の中にある部屋（配信者の防音室など）があり、繋がっている場合はどうするか
      * ドアの「ノブがある方／中心」など定義した場合、種類によってどこを原点にするか
      * 階段の部屋の場合はドアでよいか？ 階段下にするか？

