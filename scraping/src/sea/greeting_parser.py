from bs4 import BeautifulSoup
from model import Greeting


class GreetingParser:
    @staticmethod
    def parse_html(raw_html):
        """
        HTMLを受け取りグリーティング情報をリストにして返す。

        Returns:
        --------
        greeting_list : array-like(Greeting)
            Greetingオブジェクトのリスト。
        """
        soup = BeautifulSoup(raw_html, "html.parser")
        realtime_class_list = soup.find_all(class_='realtime')
        greeting_list = []
        for realtime_class in realtime_class_list:
            # 現状、「キャラクターグリーティング」という項目しか存在しないため、このループは1回しか回らない
            # ほかのタイプ（アトラクション、レストランなど）と合わせる形でメソッドを切っている
            single_segment_list = GreetingParser.__parse_single_segment(realtime_class)
            greeting_list.extend(single_segment_list)
        return greeting_list

    @staticmethod
    def __parse_single_segment(realtime_class):
        greeting_list = []
        child_list = [child for child in realtime_class.children]
        # 1つのセグメントは、待ち時間情報のリスト(ul)と更新情報(div class='update')によって構成される。
        # 待ち時間情報のリストのみ取り出す。
        ul_ = child_list[0]
        for li in ul_.children:
            attraction = GreetingParser.__parse_single_attraction(li)
            greeting_list.append(attraction)
        return greeting_list

    @staticmethod
    def __parse_single_attraction(li):
        """
        下記の形式のHTMLをParseする。

        <li>
          <a href='****' title='****'>
            <ul>
              <li class='photo'><img data-src='****' width='64' height='64' class='lozad' alt='***'></li>
              <li class='desc'>
                <h4>グリーティング名称</h4>
                <p><span class='runtime'>10:40 - 18:00</span> ただいま列に並んで利用できます</p>
              </li>
              <li class='time'>
                <p><span>待ち時間</span>20<span class='m'>分</span></p>
              </li>
            </ul>
          </a>
        </li>
        """

        greeting = Greeting()
        if elem_desc := li.find(class_='desc'):
            # グリーティング名称
            greeting.name = elem_desc.find('h4').text
            # スタンバイパスの状況
            if elem_fp := elem_desc.find(class_="fp"):
                greeting.standby_pass_status = elem_fp.text
            for child in elem_desc.children:
                if not child:
                    continue
                if not child.text:
                    continue
                # 中止フラグ
                if "中止" in child.text:
                    greeting.disable_flag = True
                # ステータス・営業時間
                if "-" in child.text and ":" in child.text:
                    start_time_str, _, end_time_str, status_str = child.text.split(" ")
                    greeting.start_time = start_time_str.strip()
                    greeting.end_time = end_time_str.strip()
                    greeting.status = status_str.strip()
                else:
                    greeting.status = child.text.strip()
        # リアルタイム待ち時間
        if elem_time := li.find(class_='time'):
            wait_time_str = elem_time.find('p').text.strip('待ち時間').strip("分")
            greeting.wait_time = int(wait_time_str)
        return greeting
