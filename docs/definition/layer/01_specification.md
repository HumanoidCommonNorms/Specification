#### Layer

開発対象を明確にするためにレイヤーを定義します。

!!! todo
    図が大きすぎなので、簡略化し詳細は章に記載する

@import "/assets/HumaroidCommonInterface/RobotLayer.puml"{width="100%"}

<div style="page-break-before:always"></div>

##### User Layer

* ユーザーが直接操作する部分であり、これは人とは限りません。例えば、他のロボットが操作することもあります。


##### AI Layer

* 認識や判断を行う部分です。

##### Application Layer

* システムを構成している部分です。
  * ROSでいうところの「NODE」に相当します。

##### Communication Layer

* 上位レイヤーからの指示を受けて、ロボットを動かす部分です。
  * プロトコルなど規約を定義します。
  * このレイヤーでは、上位指示どおり動くことを保証するものであり、独自の判断で数値を変えることはありません。

##### Physical Layer

* Controller
  * 計算能力を有するSingle Board Computer (SBC)などに相当します。
* Connector
  * ControllerとDrivenを接続するコネクタの規格を定義します。
* Driven
  * モーター・センサーなどの駆動する部分です。
* Physique
  * 外装やフレームなどに相当し、駆動機構を持たない部分です。
    * 全体を支えるフレーム
    * 外観や駆動装置を保護ための外装

