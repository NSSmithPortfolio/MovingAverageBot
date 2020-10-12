import requests
from lxml import html


def scrape_moving_average(input_url):
    data_to_return = {"moving_average": {}, "relative_strength": {}, "success": {}}
    try:
        r = requests.get(input_url, timeout=30,
                         headers={
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"})
        tree = html.fromstring(r.content)
        potential_head_els = tree.xpath("//table/thead/tr/th[text()='Period']/..")
        for potential_head_el in potential_head_els:
            header_els = potential_head_el.xpath("./th")
            if len(header_els) >= 2:
                # moving average
                if header_els[0].text_content().strip().lower() == 'period' and header_els[
                    1].text_content().strip().lower() == 'moving average' and len(
                        data_to_return["moving_average"]) == 0:
                    # it is the right table, find data elements.
                    data_row_els = potential_head_el.xpath("../following-sibling::tbody/tr")
                    for data_row_el in data_row_els:
                        period_el = data_row_el.xpath("./td[1]")
                        mov_avg_el = data_row_el.xpath("./td[2]")
                        if len(period_el) != 0 and len(mov_avg_el) != 0:
                            period_text = period_el[0].text_content().strip()  # add this
                            period_text = period_text + "MA"
                            if any(char.isdigit() for char in period_text):
                                try:
                                    probe_avg = float(mov_avg_el[0].text_content().replace(",", "").strip())  # add this
                                    data_to_return[period_text] = probe_avg
                                    data_to_return["success"] = True
                                except ValueError:
                                    continue

                # relative strength
                if header_els[0].text_content().strip().lower() == 'period' and header_els[
                    1].text_content().strip().lower() == 'relative strength' and len(
                        data_to_return["relative_strength"]) == 0:
                    # it is the right table, find data elements.
                    data_row_els = potential_head_el.xpath("../following-sibling::tbody/tr")
                    for data_row_el in data_row_els:
                        strperiod_el = data_row_el.xpath("./td[1]")
                        rel_str_el = data_row_el.xpath("./td[2]")
                        if len(strperiod_el) != 0 and len(rel_str_el) != 0:
                            str_period_text = strperiod_el[0].text_content().strip()  # add this
                            str_period_text = str_period_text + "RSI"
                            if any(char.isdigit() for char in str_period_text):
                                try:
                                    probe_strength = float(rel_str_el[0].text_content().replace(",", "").replace("%",
                                                                                                                 "").strip())  # add this
                                    data_to_return[str_period_text] = probe_strength
                                except ValueError:
                                    continue
    except:
        pass

    try:
        if data_to_return["5-DayMA"] != 0:
            data_to_return["success"] = True
    except:
        data_to_return["success"] = False
        pass

    return data_to_return


def get_url(coin):
    if coin == "ADAUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EADAUSD/technical-analysis'
    elif coin == "BATUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EBATUSD/technical-analysis'
    elif coin == "BCHUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EBCHUSD/technical-analysis'
    elif coin == "BTCUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EBTCUSD/technical-analysis'
    elif coin == "DASHUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EDASHUSD/technical-analysis'
    elif coin == "EOSUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EEOSUSD/technical-analysis'
    elif coin == "ETCUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EETCUSD/technical-analysis'
    elif coin == "ETHUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EETHUSD/technical-analysis'
    elif coin == "IOTAUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EIOTAUSD/technical-analysis'
    elif coin == "LTCUSD":
        return 'https://www.barchart.com/crypto/quotes/%5ELTCUSD/technical-analysis'
    elif coin == "NEOUSD":
        return 'https://www.barchart.com/crypto/quotes/%5ENEOUSD/technical-analysis'
    elif coin == "OMGUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EOMGUSD/technical-analysis'
    elif coin == "QTUMUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EQTUMUSD/technical-analysis'
    elif coin == "REPUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EREPUSD/technical-analysis'
    elif coin == "XLMUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EXLMUSD/technical-analysis'
    elif coin == "XRPUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EXRPUSD/technical-analysis'
    elif coin == "ZECUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EZECUSD/technical-analysis'
    elif coin == "ZRXUSD":
        return 'https://www.barchart.com/crypto/quotes/%5EZRXUSD/technical-analysis'
    else:
        print("URL not found")


def get_ma_data(coin):
    url = get_url(coin)
    ma_dict = scrape_moving_average(url)
    return ma_dict
