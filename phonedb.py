import os
import codecs
import requests
import random
import sys
from bs4 import BeautifulSoup
from requests import Request, Session

def getUserAgent():
    agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
    return agents[random.randrange(len(agents))]

def getProcessors(res,arr): 
    soup = BeautifulSoup(res.text, 'html.parser')
    for div in soup.find_all('div', "content_block_title"):
        for anchors in div.findAll('a'):
            processor = anchors.get('title')
            index = processor.find("(");
            if(index != -1):
                processor = processor[0:index]
                processor.split();
            arr.append(processor)

def getid(res,arr,elems): 
    index = res.text.find('<strong>Actions Semiconductor</strong>')
    res = res.text[index:len(res.text)] 
    index = res.find('<a id="section43"></a>')
    res = res[0:index]
    soup = BeautifulSoup(res, 'html.parser')
    for processors in soup.find_all('td'):
            for row in processors.find_all('label'): 
                for elem in elems: 
                    find = elem.split()
                    for proc in row.find_all('em'):
                        str = ""
                        for x in range(1,len(find)):
                            str += find[x] + " "
                            str.strip()
                            if(proc.text in str):
                                id = row['for']
                                id = id[3:len(id)]
                                arr.append(id)
                        
                        
def getcpukeys(ids):
    str = ""
    for id in ids:
        str += "&cpu%5B%5D=" + id
    return str

def getdevicehref(res, arr): 
    index = res.text.find('<h3>Device Specs: Search results by parameters</h3>')
    res = res.text[index:len(res.text)]
    index = res.find('<a href="#result"><strong>Jump to results</strong><img title="Jump to results" alt="Jump to results" src="icons/arrow_right.gif"></a>')
    res = res[0:index] 
    soup = BeautifulSoup(res, 'html.parser')
    for anchors in soup.find_all('div', 'content_block_title'):
        for phones in soup.find_all('a'):
            href = phones['href']
            if(href.find("specs") != -1):
                arr.append(href)
                
                
                
def extractinfo(res,arr):
    soup = BeautifulSoup(res.text, 'html.parser')
    deviceinfo = {} 
    for row in soup.find_all('tr'):
        for title in row.find_all('a'):
            if(title.get('id') == 'datasheet_item_id1'):
                deviceinfo['brand'] = title.next_element.next_element
            if(title.get('id') == 'datasheet_item_id2'):
                deviceinfo['model'] = title.next_sibling
            if(title.get('id') == 'datasheet_item_id32'):
                deviceinfo['os'] = title.next_sibling.next_sibling.get('title') 
            if(title.get('id') == 'datasheet_item_id91'):
                deviceinfo['resolution'] = title.next_sibling
            if(title.get('id') == 'datasheet_item_id87'):
                deviceinfo['dpi'] = title.next_sibling.next_element
    print('['+ str(len(arr)) + ']' + str(deviceinfo))
    arr.append(deviceinfo)
                
def main():
    req = Session()
    useragent = getUserAgent()
    url = "http://phonedb.net/index.php?m=processor&s=query&d=detailed_specs"
    instructionset = sys.argv[1]
    limit = sys.argv[2] 
    if(len(sys.argv) >= 4): 
        reset = sys.argv[3]
    data = "query_start2=&design=&type=&codename=&released_year_min=&released_year_max=&function=1&width_min=&width_max=&iset=" + instructionset +"&pipeline_min=&pipeline_max=&core_num_min=&core_num_max=&core=&abus_width_min=&abus_width_max=&bus_type%5B%5D=0&bus_clk_min=&bus_clk_max=&dbus_width_min=&dbus_width_max=&bus_ch_min=&bus_ch_max=&bus_ddr_min=&bus_ddr_max=&bus_r_min=&bus_r_max=&dbus2_width_min=&dbus2_width_max=&dma_ch_min=&dma_ch_max=&clk_min_min=&clk_min_max=&clk_max_min=&clk_max_max=&l0i_min=&l0i_max=&l0d_min=&l0d_max=&l1i_min=&l1i_max=&l1d_min=&l1d_max=&l2_min=&l2_max=&l3_min=&l3_max=&fsize_min=&fsize_max=&tech=1&transistors_min=&transistors_max=&fab=&pins_min=&pins_max=&supply_min=&supply_max=&gpu=&gpu_core_num_min=&gpu_core_num_max=&gpu_clk_min=&gpu_clk_max=&vram_min=&vram_max=&p_r%5B%5D=0&gps%5B%5D=0&galileo%5B%5D=0&glonass%5B%5D=0&bds%5B%5D=0&plus="
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.5',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'phonedb.net',
        'Origin':'http://phonedb.net',
        'Referer':'http://phonedb.net/index.php?m=processor&s=query&d=detailed_specs&i=1',
        'User-Agent': useragent
    }
    res = req.post(url,data=data,headers=headers)
    processors = []
    getProcessors(res,processors);
    processors.sort()
    headers['Referer'] = 'http://phonedb.net/index.php?m=device&s=query' 
    url = 'http://phonedb.net/index.php?m=device&s=query&d=detailed_specs&i=1'
    data = 'brand=&model=&released_min=&released_max=&cat=1&width_min=&width_max=&height_min=&height_max=&depth_min=&depth_max=&depth_i_min=&depth_i_max=&mass_min=&mass_max=&mass_oz_min=&mass_oz_max=&os_family=1&sw_e%5B%5D=0&expand_section35=&cpu_clk_min=&cpu_clk_max=&ram_type=1&ram_cap_min=&ram_cap_max=&ram_cap_b=&rom_cap_min=&rom_cap_max=&rom_cap_b=&d_res=&d_px_min=&d_px_max=&d_py_min=&d_py_max=&d_diag_i_min=&d_diag_i_max=&d_type=0&gpu_clk_min=&gpu_clk_max=&p_r%5B%5D=0&p_dual=0&ts=0&tp=0&kb=0&exp%5B%5D=0&usb_c=0&bt=0&wlan%5B%5D=0&nfc%5B%5D=0&radio_rx=0&gps%5B%5D=0&gps_e%5B%5D=0&c_px_min=&c_px_max=&c_py_min=&c_py_max=&c_focus%5B%5D=0&c_vres=&c_flash=0&c_e%5B%5D=0&cd_sensor=0&c2_pn=&c2_focus%5B%5D=0&c2_flash=0&b_build=0&b_cap_min=&b_cap_max=&country%5B%5D=0'
    res = req.post(url,data=data,headers=headers)
    ids = []
    getid(res, ids, processors)
    url = 'http://phonedb.net/index.php?m=device&s=query&d=detailed_specs'
    headers['Referer'] = 'http://phonedb.net/index.php?m=device&s=query&d=detailed_specs&i=1' 
    cpukey = getcpukeys(ids)
    data  = 'query_start2=&brand=&model=&released_min=' + '&released_max=&design=&manufacturer=&codename=&oemid=&hw_e%5B%5D=0&cat=1&width_min=&width_max=&width_i_min=&width_i_max=&height_min=&height_max=&height_i_min=&height_i_max=&depth_min=&depth_max=&depth_i_min=&depth_i_max=&volume_min=&volume_max=&mass_min=&mass_max=&mass_oz_min=&mass_oz_max=&os_family=141&sw_e%5B%5D=0&cpu_clk_min=&cpu_clk_max=' + cpukey + '&ram_type=1&ram_clk_min=&ram_clk_max=&ram_cap_min=&ram_cap_max=&ram_cap_b=&ram_free_min=&ram_free_max=&ram_chip=&rom_type=0&rom_cap_min=&rom_cap_max=&rom_cap_b=&rom_chip=&rom2_cap_min=&rom2_cap_max=&rom2_cap_b=&hdd_cap_min=&hdd_cap_max=&d_px_min=&d_px_max=&d_py_min=&d_py_max=&d_diag_i_min=&d_diag_i_max=&d_bezel_min=&d_bezel_max=&d_util_min=&d_util_max=&d_notch_min=&d_notch_max=&d_hole_min=&d_hole_max=&d_ppi_min=&d_ppi_max=&d_type=0&d_subtype=0&d_depth_min=&d_depth_max=&d_lit=0&d_refl=0&d_subpixel=0&d_refresh_min=&d_refresh_max=&d_sr=0&d2_px_min=&d2_px_max=&d2_py_min=&d2_py_max=&d2_diag_i_min=&d2_diag_i_max=&d2_type=0&d2_depth_min=&d2_depth_max=&graphics_chip=&gpu_clk_min=&gpu_clk_max=&av_out_type=0&av_out_c=0&av_out_res=0&av_in_type=0&av_in_c=0&au_ch=0&au_chip=&au_ad_min=&au_ad_max=&au_ad_sr_min=&au_ad_sr_max=&mic=0&au_in=0&au_da_min=&au_da_max=&au_da_sr_min=&au_da_sr_max=&speaker=0&speaker_pwr_min=&speaker_pwr_max=&au_out=0&p_net%5B%5D=0&p_r%5B%5D=0&p_card%5B%5D=0&ring=0&hac%5B%5D=0&p_e%5B%5D=0&p_chip=&p_dual=0&p2_card=0&p2_r%5B%5D=0&ts=0&ts_points=0&tp=0&tp_points=0&kb=0&kb_bl=0&kb_num_min=&kb_num_max=&dpad=0&jog=0&exp%5B%5D=0&usb_v=0&usb_r%5B%5D=0&usb_e%5B%5D=0&usb_c=0&usb_chr_p_min=&usb_chr_p_max=&bt=0&bt_p%5B%5D=0&bt_chip=&wlan%5B%5D=0&wlan_e%5B%5D=0&wlan_chip=&wman%5B%5D=0&nfc%5B%5D=0&ir=0&ir_r=0&ser=0&ser_c=0&ser_r=0&lan=0&lan_c=0&modem=0&modem_c=0&fax=0&tv%5B%5D=0&tv_a=0&radio_rx=0&radio_a=0&radio_tx=0&dmb%5B%5D=0&dmb_a=0&gps%5B%5D=0&gps_ch_min=&gps_ch_max=&gps_a=0&gps_e%5B%5D=0&glonass%5B%5D=0&galileo%5B%5D=0&bds%5B%5D=0&n_chip=&c_module=&c_sensor=0&c_format_min=&c_format_max=&c_p_size_min=&c_p_size_max=&c_px_min=&c_px_max=&c_py_min=&c_py_max=&c_pn=&c_apert_w_min=&c_apert_w_max=&c_apert_t_min=&c_apert_t_max=&c_zoom_min=&c_zoom_max=&c_dzoom_min=&c_dzoom_max=&c_focus%5B%5D=0&c_efl_min_min=&c_efl_min_max=&c_efl_max_min=&c_efl_max_max=&c_vpx_min=&c_vpx_max=&c_vpy_min=&c_vpy_max=&c_flash=0&c_e%5B%5D=0&cd_sensor=0&cd_p_size_min=&cd_p_size_max=&cd_px_min=&cd_px_max=&cd_py_min=&cd_py_max=&cd_pn=&cd_apert_w_min=&cd_apert_w_max=&cd_focus%5B%5D=0&cd_e%5B%5D=0&cd2_sensor=0&cd2_px_min=&cd2_px_max=&cd2_py_min=&cd2_py_max=&cd2_pn=&cd2_apert_w_min=&cd2_apert_w_max=&cd3_sensor=0&cd4_sensor=0&c2_module=&c2_sensor=0&c2_format_min=&c2_format_max=&c2_p_size_min=&c2_p_size_max=&c2_px_min=&c2_px_max=&c2_py_min=&c2_py_max=&c2_pn=&c2_apert_w_min=&c2_apert_w_max=&c2_focus%5B%5D=0&c2_vpx_min=&c2_vpx_max=&c2_vpy_min=&c2_vpy_max=&c2_flash=0&c2_e%5B%5D=0&c2d_sensor=0&c2d_p_size_min=&c2d_p_size_max=&c2d_px_min=&c2d_px_max=&c2d_py_min=&c2d_py_max=&c2d_apert_w_min=&c2d_apert_w_max=&c2d2_sensor=0&c2d2_px_min=&c2d2_px_max=&c2d2_py_min=&c2d2_py_max=&c2d2_apert_w_min=&c2d2_apert_w_max=&compass=0&acc=0&gyro=0&sensor%5B%5D=0&bcs%5B%5D=0&ipf=1&ips=1&ipt_min=&ipt_max=&ipi_min=&ipi_max=&ipit_min=&ipit_max=&mil=0&b_type=0&b_build=0&b_volt_min=&b_volt_max=&b_cap_min=&b_cap_max=&b_energy_min=&b_energy_max=&b_time_min=&b_time_max=&b_time_sby_min=&b_time_sby_max=&b_time_talk_min=&b_time_talk_max=&wlc%5B%5D=0&wlc_chr_p_min=&wlc_chr_p_max=&country%5B%5D=0&region%5B%5D=0'
    res = req.post(url,data=data,headers=headers)
    links = [] 
    getdevicehref(res, links)
    del headers['Content-Type']
    headers['Referer'] = url
    base = "http://phonedb.net/"
    info = []
    if(bool(reset) == 1):
        if(os.path.exists("phones.txt")):
            os.remove("phones.txt")
        else:
            print("Supplied reset arg without phones.txt file.")
    f = codecs.open("phones.txt",'w+', encoding='utf8')
    for link in links:
        url = base + link;
        res = req.get(url=url,headers=headers)
        extractinfo(res,info)
        if(int(limit) == len(info)):
            break
    for phone in info:
        f.write(str(phone))
    f.close()
    
    
if __name__ == "__main__":
    main()
