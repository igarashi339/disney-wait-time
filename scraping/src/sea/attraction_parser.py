from bs4 import BeautifulSoup
from model import Attraction


class AttractionParser:
    @staticmethod
    def parse_html(raw_html):
        """
        HTMLを受け取りアトラクション情報をリストにして返す。

        Returns:
        --------
        attraction_list : array-like(Attraction)
            Attractionオブジェクトのリスト。
        """
        soup = BeautifulSoup(raw_html, "html.parser")
        realtime_class_list = soup.find_all(class_='realtime')
        attraction_list = []
        for realtime_class in realtime_class_list:
            # 「人気のアトラクション」「メディテレーニアンハーバー」「ポートディスカバリー」「マーメイドラグーン」
            # の4つのセグメントに分かれているため、それぞれをParseしたものを合算する
            single_segment_list = AttractionParser.__parse_single_segment(realtime_class)
            attraction_list.extend(single_segment_list)
        return attraction_list

    @staticmethod
    def __parse_single_segment(realtime_class):
        attraction_list = []
        child_list = [child for child in realtime_class.children]
        # 1つのセグメントは、待ち時間情報のリスト(ul)と更新情報(div class='update')によって構成される。
        # 待ち時間情報のリストのみ取り出す。
        ul_ = child_list[0]
        for li in ul_.children:
            attraction = AttractionParser.__parse_single_attraction(li)
            attraction_list.append(attraction)
        return attraction_list

    @staticmethod
    def __parse_single_attraction(li):
        """
        下記の形式のHTMLをParseする。

        <li>
          <a href='****' title='****の待ち時間'>
            <ul>
              <li class='photo'><img data-src='****' width='64' height='64' class='lozad' alt='****'></li>
              <li class='desc'>
                <h4>アトラクション名称</h4>
                <p><span class='fp'>発券中 12:00-12:30</span></p>
                <p>スタンバイパスがある方のみ案内中<br> <span class='runtime'>10:00-19:00</span></p>
              </li>
              <li class='time'>
                <p><span>待ち時間</span>20<span class='m'>分</span></p>
              </li>
            </ul>
          </a>
        </li>
        """

        attraction = Attraction()
        if elem_desc := li.find(class_='desc'):
            # アトラクション名称
            attraction.name = elem_desc.find('h4').text
            # スタンバイパスの状況
            if elem_fp := elem_desc.find(class_="fp"):
                attraction.standby_pass_status = elem_fp.text
            for child in elem_desc.children:
                if not child:
                    continue
                if not child.text:
                    continue
                # 中止フラグ
                if "中止" in child.text:
                    attraction.disable_flag = True
                # ステータス・営業時間
                if "-" in child.text and ":" in child.text:
                    attraction.status, start_end_time = child.text.split(" ")
                    attraction.start_time,  attraction.end_time = start_end_time.split("-")

        # リアルタイム待ち時間
        if elem_time := li.find(class_='time'):
            wait_time_str = elem_time.find('p').text.strip('待ち時間').strip("分")
            attraction.wait_time = int(wait_time_str)
        return attraction
