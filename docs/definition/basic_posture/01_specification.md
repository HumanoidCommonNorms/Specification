#### 基本姿勢

##### ポーズ

人型ロボットの基本姿勢を定義する場合は、下記の三つのポーズが考えられる。

<table>
<tr>
<th>T字ポーズ</th>
<th>A字ポーズ</th>
<th>気を付けポーズ</th>
</tr>
<tr>
<td>
    <img src="/assets/HumaroidCommonInterface/basic_posture_t.png" alt="T字ポーズ" style="max-width:10em;max-height:10em" />
</td>
<td>
    <img src="/assets/HumaroidCommonInterface/basic_posture_a.png" alt="T字ポーズ" style="max-width:10em;max-height:10em" />
</td>
<td>
    <img src="/assets/HumaroidCommonInterface/basic_posture_upright.png" alt="T字ポーズ" style="max-width:10em;max-height:10em" />
</td>
</tr>
</table>

T字ポーズなど3DCGなどのモデリングソフトウェアでの基本ポーズは、
人間と特異なポーズのため人間がもっとも楽なポーズを基準にすべきという意見もある。

ただし、以下の理由から、T字ポーズを基本姿勢とする。

* 筐体の問題で、手を真下に下した状態が取れないロボットがいる。
* 人体として「お腹の中の赤ちゃん」と同様の丸まった姿勢が一番楽な姿勢という意見があるが、それを基本姿勢にしてよいものか？

**内部データとして**T字ポーズを基本姿勢としてるが、
各ロボットの基本姿勢は、T字ポーズの差分をキャリブレーションデータとして保持し、もっとも楽な姿勢を基本姿勢とする。



##### 座標

手足などの座標は、両肩の中心を原点とし、中心からの角度で表す。

@import "/assets/HumaroidCommonInterface/basic_posture_top.png"{height="200em"}

理由は**関節**の角度,稼働範囲比率,SI単位系(mmなど)で表すと、
拍手などの体の中心で手を合わせるモーションなどの流用が出来ず、個々の筐体の固有データになるため。

@import "/assets/HumaroidCommonInterface/basic_posture_applause.png"{height="200em"}

