#### 基本姿勢

共通で扱う内部データは、下記を基本姿勢とする。

* T字ポーズ
  * 腕
    * 手は地面に水平に伸ばす
    * 手のひらは下向き
    * 肘が曲がる部分は後ろ（背中側）
    * 足は肩幅に開く
  * 腰
    * 背筋を伸ばす
    * 腰はそらさない
  * 足
    * 膝を伸ばす
    * 足首は踵を上げない
    * 足の裏は地面につける
    * 重心は踵から指先にかけて均等にかかる
    * 足の指は前に向ける
    * 足は肩幅まで開く
@import "/assets/HumaroidCommonInterface/basic_posture_t.png"{height="200em"}

腕の座標は両肩の中心を原点とし、中心からの角度で表す。

@import "/assets/HumaroidCommonInterface/basic_posture_top.png"{height="200em"}


自作ロボットの基本姿勢は、T字ポーズの差分を筐体固有補正として保持し、もっとも楽な姿勢を基本姿勢とする。

@import "/assets/HumaroidCommonInterface/basic_posture_upright.png"{height="200em"}



上記のことを踏まえて、筐体の姿勢は下記のように表す。

```math
筐体の姿勢=基本姿勢+筐体固有補正データ+キャリブレーションデータ
```
