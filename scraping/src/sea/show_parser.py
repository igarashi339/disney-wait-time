from bs4 import BeautifulSoup
from model import Show


class ShowParser:
    @staticmethod
    def parse_html(raw_html):
        """
        HTMLを受け取りショー情報をリストにして返す。

        Returns:
        --------
        show_list : array-like(Show)
            Showオブジェクトのリスト。
        """
        soup = BeautifulSoup(raw_html, "html.parser")
        realtime_class_list = soup.find_all(class_='realtime')
        show_list = []
        for realtime_class in realtime_class_list:
            # 現状、「ショー」という項目しか存在しないため、このループは1回しか回らない
            # ほかのタイプ（アトラクション、レストランなど）と合わせる形でメソッドを切っている
            single_segment_list = ShowParser.__parse_single_segment(realtime_class)
            show_list.extend(single_segment_list)
        return show_list

    @staticmethod
    def __parse_single_segment(realtime_class):
        show_list = []
        child_list = [child for child in realtime_class.children]
        # 1つのセグメントは、待ち時間情報のリスト(ul)と更新情報(div class='update')によって構成される。
        # 待ち時間情報のリストのみ取り出す。
        ul_ = child_list[0]
        for li in ul_.children:
            attraction = ShowParser.__parse_single_attraction(li)
            show_list.append(attraction)
        return show_list

    @staticmethod
    def __parse_single_attraction(li):
        """
        下記の形式のHTMLをParseする。

        <li>
          <a href='****' title='****'>
            <ul>
              <li class='photo'><img data-src='****' width='64' height='64' class='lozad' alt='***'></li>
              <li class='desc'>
                <h4>ショー名称</h4>
                <p>11:15 12:40 <span class='cur'>14:40</span> 16:05</p>
              </li>
              <li class='time'>
                <p><span>開始</span>14:40</p>
              </li>
            </ul>
          </a>
        </li>
        """

        show = Show()
        if elem_desc := li.find(class_='desc'):
            # ショー名称
            show.name = elem_desc.find('h4').text
            for child in elem_desc.children:
                if not child:
                    continue
                if not child.text:
                    continue
                # 中止フラグ
                if "中止" in child.text:
                    show.disable_flag = True
                # ショー開始時間一覧
                show.start_time_list = []
                start_time_list = child.text.split(" ")
                for start_time in start_time_list:
                    if ":" in start_time:
                        show.start_time_list.append(start_time)

        # 次のショー開始時刻
        if elem_time := li.find(class_='time'):
            show.next_start_time = elem_time.find('p').text.strip('開始')
        return show
