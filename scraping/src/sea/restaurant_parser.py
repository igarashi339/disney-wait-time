from bs4 import BeautifulSoup
from model import Restaurant


class RestaurantParser:
    @staticmethod
    def parse_html(raw_html):
        """
        HTMLを受け取りレストラン情報をリストにして返す。

        Returns:
        --------
        restaurant_list : array-like(Restaurant)
            Restaurantオブジェクトのリスト。
        """
        soup = BeautifulSoup(raw_html, "html.parser")
        realtime_class_list = soup.find_all(class_='realtime')
        restaurant_list = []
        for realtime_class in realtime_class_list:
            # 「人気のレストラン」「メディテレーニアンハーバー」「アメリカンウォーターフロント」「アラビアンコースト」
            # の4つのセグメントに分かれているため、それぞれをParseしたものを合算する
            single_segment_list = RestaurantParser.__parse_single_segment(realtime_class)
            restaurant_list.extend(single_segment_list)
        return restaurant_list

    @staticmethod
    def __parse_single_segment(realtime_class):
        restaurant_list = []
        child_list = [child for child in realtime_class.children]
        # 1つのセグメントは、待ち時間情報のリスト(ul)と更新情報(div class='update')によって構成される。
        # 待ち時間情報のリストのみ取り出す。
        ul_ = child_list[0]
        for li in ul_.children:
            attraction = RestaurantParser.__parse_single_restaurant(li)
            restaurant_list.append(attraction)
        return restaurant_list

    @staticmethod
    def __parse_single_restaurant(li):
        """
        下記の形式のHTMLをParseする。

        <li>
          <a href='****' title='****の待ち時間'>
            <ul>
              <li class='photo'><img data-src='****' width='64' height='64' class='lozad' alt='***'></li>
              <li class='desc'>
                <h4>レストラン名称</h4>
                <p>運営ステータス<br> <span class='runtime'>11:00-17:45</span></p>
              </li>
            </ul>
          </a>
        </li>
        """
        restaurant = Restaurant()
        if elem_desc := li.find(class_='desc'):
            # レストラン名称
            restaurant.name = elem_desc.find('h4').text
            for child in elem_desc.children:
                if not child:
                    continue
                if not child.text:
                    continue
                # 中止フラグ
                if "中止" in child.text:
                    restaurant.disable_flag = True
                # ステータス・営業時間
                if "-" in child.text and ":" in child.text:
                    restaurant.status, start_end_time = child.text.split(" ")
                    restaurant.start_time, restaurant.end_time = start_end_time.split("-")
                else:
                    restaurant.status = child.text.strip()
            # リアルタイム待ち時間
            if elem_time := li.find(class_='time'):
                wait_time_str = elem_time.find('p').text.strip('待ち時間').strip("分")
                # 時間に幅がある場合は最も大きい値をとる
                if "-" in wait_time_str:
                    wait_time_str = wait_time_str.split("-")[-1]
                restaurant.wait_time = int(wait_time_str)
        return restaurant
