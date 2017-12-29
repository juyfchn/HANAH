# -*- coding: UTF-8 -*-
import execjs
import json
import logging
import random
import re
import requests
import time

import FileUtils


class WenShu:
    def __init__(self):
        # Init default parameters
        self.item_in_page = 20
        self.case_brief = dict()
        
        # Init log
        self._init_log()
        
        # Init url list 
        self.url_list = {'list_url':'http://wenshu.court.gov.cn/list/list/',
                        'waf_captcha_url':'http://wenshu.court.gov.cn/waf_captcha/',
                        'waf_verify_url':'http://wenshu.court.gov.cn/waf_verify.htm',
                        'list_content_url':'http://wenshu.court.gov.cn/List/ListContent',
                        'validate_code_url':'http://wenshu.court.gov.cn/User/ValidateCode',
                        'check_visit_code_url':'http://wenshu.court.gov.cn/Content/CheckVisitCode',
                        'create_code_url':'http://wenshu.court.gov.cn/ValiCode/CreateCode/'
        }
        
        
        # Init default header
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'X-Forwarded-For':  '{}.{}.{}.{},153.88.176.160'.format(random.randint(1, 254),
                                                                    random.randint(1, 254),
                                                                    random.randint(1, 254),
                                                                    random.randint(1, 254))
        }
        
        # Load ua list
        with open('ua_list.json', 'r') as f:
            self.ua_list = json.load(f)
        
        # Init default session
        self.sess, self.vl5x = self.get_sess()
    
    
    def _init_log(self):
        # Create logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

        
    def get_sess(self):
        sess = requests.Session()
        # 获取form表单的参数
        post = execjs.compile("""
                var hexcase = 0;  
                var b64pad  = ""; 
                var chrsz   = 8;  
                function hex_md5(s){ return binl2hex(core_md5(str2binl(s), s.length * chrsz));}
                function b64_md5(s){ return binl2b64(core_md5(str2binl(s), s.length * chrsz));}
                function str_md5(s){ return binl2str(core_md5(str2binl(s), s.length * chrsz));}
                function hex_hmac_md5(key, data) { return binl2hex(core_hmac_md5(key, data)); }
                function b64_hmac_md5(key, data) { return binl2b64(core_hmac_md5(key, data)); }
                function str_hmac_md5(key, data) { return binl2str(core_hmac_md5(key, data)); }
            
                function md5_vm_test()
                {
                return hex_md5("abc") == "900150983cd24fb0d6963f7d28e17f72";
                }
            
                function core_md5(x, len)
                {
                x[len >> 5] |= 0x80 << ((len) % 32);
                x[(((len + 64) >>> 9) << 4) + 14] = len;
            
                var a =  1732584193;
                var b = -271733879;
                var c = -1732584194;
                var d =  271733878;
            
                for(var i = 0; i < x.length; i += 16)
                {
                    var olda = a;
                    var oldb = b;
                    var oldc = c;
                    var oldd = d;
            
                    a = md5_ff(a, b, c, d, x[i+ 0], 7 , -680876936);
                    d = md5_ff(d, a, b, c, x[i+ 1], 12, -389564586);
                    c = md5_ff(c, d, a, b, x[i+ 2], 17,  606105819);
                    b = md5_ff(b, c, d, a, x[i+ 3], 22, -1044525330);
                    a = md5_ff(a, b, c, d, x[i+ 4], 7 , -176418897);
                    d = md5_ff(d, a, b, c, x[i+ 5], 12,  1200080426);
                    c = md5_ff(c, d, a, b, x[i+ 6], 17, -1473231341);
                    b = md5_ff(b, c, d, a, x[i+ 7], 22, -45705983);
                    a = md5_ff(a, b, c, d, x[i+ 8], 7 ,  1770035416);
                    d = md5_ff(d, a, b, c, x[i+ 9], 12, -1958414417);
                    c = md5_ff(c, d, a, b, x[i+10], 17, -42063);
                    b = md5_ff(b, c, d, a, x[i+11], 22, -1990404162);
                    a = md5_ff(a, b, c, d, x[i+12], 7 ,  1804603682);
                    d = md5_ff(d, a, b, c, x[i+13], 12, -40341101);
                    c = md5_ff(c, d, a, b, x[i+14], 17, -1502002290);
                    b = md5_ff(b, c, d, a, x[i+15], 22,  1236535329);
            
                    a = md5_gg(a, b, c, d, x[i+ 1], 5 , -165796510);
                    d = md5_gg(d, a, b, c, x[i+ 6], 9 , -1069501632);
                    c = md5_gg(c, d, a, b, x[i+11], 14,  643717713);
                    b = md5_gg(b, c, d, a, x[i+ 0], 20, -373897302);
                    a = md5_gg(a, b, c, d, x[i+ 5], 5 , -701558691);
                    d = md5_gg(d, a, b, c, x[i+10], 9 ,  38016083);
                    c = md5_gg(c, d, a, b, x[i+15], 14, -660478335);
                    b = md5_gg(b, c, d, a, x[i+ 4], 20, -405537848);
                    a = md5_gg(a, b, c, d, x[i+ 9], 5 ,  568446438);
                    d = md5_gg(d, a, b, c, x[i+14], 9 , -1019803690);
                    c = md5_gg(c, d, a, b, x[i+ 3], 14, -187363961);
                    b = md5_gg(b, c, d, a, x[i+ 8], 20,  1163531501);
                    a = md5_gg(a, b, c, d, x[i+13], 5 , -1444681467);
                    d = md5_gg(d, a, b, c, x[i+ 2], 9 , -51403784);
                    c = md5_gg(c, d, a, b, x[i+ 7], 14,  1735328473);
                    b = md5_gg(b, c, d, a, x[i+12], 20, -1926607734);
            
                    a = md5_hh(a, b, c, d, x[i+ 5], 4 , -378558);
                    d = md5_hh(d, a, b, c, x[i+ 8], 11, -2022574463);
                    c = md5_hh(c, d, a, b, x[i+11], 16,  1839030562);
                    b = md5_hh(b, c, d, a, x[i+14], 23, -35309556);
                    a = md5_hh(a, b, c, d, x[i+ 1], 4 , -1530992060);
                    d = md5_hh(d, a, b, c, x[i+ 4], 11,  1272893353);
                    c = md5_hh(c, d, a, b, x[i+ 7], 16, -155497632);
                    b = md5_hh(b, c, d, a, x[i+10], 23, -1094730640);
                    a = md5_hh(a, b, c, d, x[i+13], 4 ,  681279174);
                    d = md5_hh(d, a, b, c, x[i+ 0], 11, -358537222);
                    c = md5_hh(c, d, a, b, x[i+ 3], 16, -722521979);
                    b = md5_hh(b, c, d, a, x[i+ 6], 23,  76029189);
                    a = md5_hh(a, b, c, d, x[i+ 9], 4 , -640364487);
                    d = md5_hh(d, a, b, c, x[i+12], 11, -421815835);
                    c = md5_hh(c, d, a, b, x[i+15], 16,  530742520);
                    b = md5_hh(b, c, d, a, x[i+ 2], 23, -995338651);
            
                    a = md5_ii(a, b, c, d, x[i+ 0], 6 , -198630844);
                    d = md5_ii(d, a, b, c, x[i+ 7], 10,  1126891415);
                    c = md5_ii(c, d, a, b, x[i+14], 15, -1416354905);
                    b = md5_ii(b, c, d, a, x[i+ 5], 21, -57434055);
                    a = md5_ii(a, b, c, d, x[i+12], 6 ,  1700485571);
                    d = md5_ii(d, a, b, c, x[i+ 3], 10, -1894986606);
                    c = md5_ii(c, d, a, b, x[i+10], 15, -1051523);
                    b = md5_ii(b, c, d, a, x[i+ 1], 21, -2054922799);
                    a = md5_ii(a, b, c, d, x[i+ 8], 6 ,  1873313359);
                    d = md5_ii(d, a, b, c, x[i+15], 10, -30611744);
                    c = md5_ii(c, d, a, b, x[i+ 6], 15, -1560198380);
                    b = md5_ii(b, c, d, a, x[i+13], 21,  1309151649);
                    a = md5_ii(a, b, c, d, x[i+ 4], 6 , -145523070);
                    d = md5_ii(d, a, b, c, x[i+11], 10, -1120210379);
                    c = md5_ii(c, d, a, b, x[i+ 2], 15,  718787259);
                    b = md5_ii(b, c, d, a, x[i+ 9], 21, -343485551);
            
                    a = safe_add(a, olda);
                    b = safe_add(b, oldb);
                    c = safe_add(c, oldc);
                    d = safe_add(d, oldd);
                }
                return Array(a, b, c, d);
            
                }
            
                function md5_cmn(q, a, b, x, s, t)
                {
                return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s),b);
                }
                function md5_ff(a, b, c, d, x, s, t)
                {
                return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t);
                }
                function md5_gg(a, b, c, d, x, s, t)
                {
                return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t);
                }
                function md5_hh(a, b, c, d, x, s, t)
                {
                return md5_cmn(b ^ c ^ d, a, b, x, s, t);
                }
                function md5_ii(a, b, c, d, x, s, t)
                {
                return md5_cmn(c ^ (b | (~d)), a, b, x, s, t);
                }
                function core_hmac_md5(key, data)
                {
                var bkey = str2binl(key);
                if(bkey.length > 16) bkey = core_md5(bkey, key.length * chrsz);
            
                var ipad = Array(16), opad = Array(16);
                for(var i = 0; i < 16; i++)
                {
                    ipad[i] = bkey[i] ^ 0x36363636;
                    opad[i] = bkey[i] ^ 0x5C5C5C5C;
                }
            
                var hash = core_md5(ipad.concat(str2binl(data)), 512 + data.length * chrsz);
                return core_md5(opad.concat(hash), 512 + 128);
                }
            
                function safe_add(x, y)
                {
                var lsw = (x & 0xFFFF) + (y & 0xFFFF);
                var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
                return (msw << 16) | (lsw & 0xFFFF);
                }
            
                function bit_rol(num, cnt)
                {
                return (num << cnt) | (num >>> (32 - cnt));
                }
            
                function str2binl(str)
                {
                var bin = Array();
                var mask = (1 << chrsz) - 1;
                for(var i = 0; i < str.length * chrsz; i += chrsz)
                    bin[i>>5] |= (str.charCodeAt(i / chrsz) & mask) << (i%32);
                return bin;
                }
            
                function binl2str(bin)
                {
                var str = "";
                var mask = (1 << chrsz) - 1;
                for(var i = 0; i < bin.length * 32; i += chrsz)
                    str += String.fromCharCode((bin[i>>5] >>> (i % 32)) & mask);
                return str;
                }
            
                function binl2hex(binarray)
                {
                var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
                var str = "";
                for(var i = 0; i < binarray.length * 4; i++)
                {
                    str += hex_tab.charAt((binarray[i>>2] >> ((i%4)*8+4)) & 0xF) +
                        hex_tab.charAt((binarray[i>>2] >> ((i%4)*8  )) & 0xF);
                }
                return str;
                }
            
                function binl2b64(binarray)
                {
                var tab = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
                var str = "";
                for(var i = 0; i < binarray.length * 4; i += 3)
                {
                    var triplet = (((binarray[i   >> 2] >> 8 * ( i   %4)) & 0xFF) << 16)
                                | (((binarray[i+1 >> 2] >> 8 * ((i+1)%4)) & 0xFF) << 8 )
                                |  ((binarray[i+2 >> 2] >> 8 * ((i+2)%4)) & 0xFF);
                    for(var j = 0; j < 4; j++)
                    {
                    if(i * 8 + j * 6 > binarray.length * 32) str += b64pad;
                    else str += tab.charAt((triplet >> 6*(3-j)) & 0x3F);
                    }
                }
                return str;
                }
            
                function hex_md5(s){ return binl2hex(core_md5(str2binl(s), s.length * chrsz));}
            
                function getKey(vjkl5){
                var i=25-10-8-2;
                var c=vjkl5;
                var str=c.substr(i,i*5)+c.substr((i+1)*(i+1),3);
                var a=str.substr(i)+str.substr(-4);
                var b=str.substr(4)+a.substr(-i-1);
                c=hex_md5(str).substr(i-1,24);
                return c
                }
            
                """)
        # 当网站访问量过大时 会有302重定向到验证码页面 需要输入验证码 获取session
        while True:
            try:
                response = sess.get(self.url_list['list_url'],
                                    headers=self.header,
                                    allow_redirects=False)
                self.logger.debug("Response status code is {}".format(response.status_code))
                if response.status_code == 200:
                    vjkl5 = response.cookies.get_dict()['vjkl5']
                    vl5x = post.call('getKey', vjkl5)
                    self.logger.debug("vjkl5 is %s and vl5x is %s" % (vjkl5, vl5x))
                    return sess, vl5x
                if response.status_code == 503:
                    # 服务器出现问题
                    self.logger.debug('the service is bad and response_status_code is {}, wait one minute retry'.format(response.status_code))
                    time.sleep(60)
                    continue
                if response.status_code == 302:
                    while True:
                        # 302重定向 需要输入验证码
                        home_yzm = sess.get(self.url_list['waf_captcha_url'], 
                                            headers=headers,
                                            allow_redirects=False, 
                                            timeout=10)
                        if home_yzm.status_code >= 500:
                            # 服务器出现问题
                            self.logger.debug('the service is bad and response_status_code is {}, wait one minute retry'.format(response.status_code))
                            time.sleep(60)
                            continue
                        with open('captcha.jpg', 'wb') as f:
                            f.write(home_yzm.content)
                        #captcha = result_captcha('captcha.jpg')
                        # TODO: Get code automatically
                        captcha = input("Enter code: ")
                        verify_response = sess.get(self.url['waf_verify_url'] + '?captcha={}'.format(captcha),
                                                headers=headers, 
                                                allow_redirects=False)
                        try:
                            value = verify_response.cookies.get_dict()['wafverify']
                        except Exception as e:
                            # 验证码输入出错 response没有wafverify字段 重试
                            self.logger.debug(e)
                            continue
                        vjkl5 = sess.cookies.get_dict()['vjkl5']
                        vl5x = post.call('getKey', vjkl5)
                        return sess, vl5x
            except Exception as e:
                self.logger.debug(e)
                continue
                
               
    def setSearchCriteria(self, search_criteria):
        self.logger.info("Set search criteria to {}".format(search_criteria))
        self.search_criteria = search_criteria
        

    def get_captcha(self):
        while True:
            try:
                # 获取验证码 发送验证码 验证guid
                yzm = execjs.compile('''
                function createGuid() {
                    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
                }
                function ref() {
                    var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid(); //CreateGuid();
                    return guid;
                }
                ''')
                guid = yzm.call('ref')
                self.logger.debug("guid is {}".format(guid))

                header = self.header
                header['User-Agent'] = random.choice(self.ua_list)
                yzm = self.sess.get(self.url_list['create_code_url'] + '?guid={}'.format(guid), headers=header, allow_redirects=False)
                self.logger.debug("yzm is {}".format(yzm))
                if yzm.status_code == 302:
                    self.sess, self.vl5x = self.get_sess()
                    continue
                if yzm.status_code >= 500:
                    self.logger.debug('the service is bad and response_status_code is {}, wait one minute retry'.format(yzm.status_code))
                    time.sleep(60)
                    continue
                with open('captcha.jpg', 'wb') as f:
                    f.write(yzm.content)
                # captcha = yundama.result_captcha('captcha.jpg')
                # Todo: use automatically way to get code
                captcha = input("Enter code: ")
                return captcha, guid
            except Exception as e:
                print('get captcah bad retry again')
                print(e)

              
    def get_total_item_number(self):
        raw = self.get_first_page()
        self.logger.debug(raw)                
        total_number = re.search('"Count":"([0-9]+)"', raw)
        if total_number:
            self.total_items = int(total_number.group(1))

            
    def get_first_page(self):
        return self.get_page(1)
    
    
    def get_guid(self):
        #获取guid参数
        js1 = '''
            function getGuid() {
                var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid(); //CreateGuid();
                return guid;
            }
            var createGuid = function () {
                return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
            }
        '''
        ctx1 = execjs.compile(js1)
        guid = (ctx1.call("getGuid"))
        return guid
    
    
    def get_number(self, guid):
        ###获取number
        codeUrl = "http://wenshu.court.gov.cn/ValiCode/GetCode"
        data = {
            'guid':guid
        }
        req1 = self.sess.post(codeUrl,data=data)
        number = req1.text
        return number
    
    
    def get_page(self, index=1):
        i = 0
        while i < 5:
            #captcha, guid = self.get_captcha()  # 每次请求都要用到
            guid = self.get_guid()
            number = self.get_number(guid)
            self.logger.debug("guid: {}, number: {}".format(guid, number))
            
            form_data = {
                'Param': self.search_criteria,
                'Index': index,
                'Page': 20,
                'Order': '法院层级',
                'Direction': 'asc',
                'vl5x': self.vl5x,
                'number': number,
                'guid': guid,
            }
            try:
                header = self.header
                header['User-Agent'] = random.choice(self.ua_list)
                response = self.sess.post(self.url_list['list_content_url'], headers=header, data=form_data)
                if response.status_code == 302:
                    self.sess, self.vl5x = self.get_sess()
                    continue
                if response.status_code >= 500:
                    self.logger.info('the service is bad and response_status_code is {}, wait one minute retry'.format(response.status_code))
                    time.sleep(60)
                    continue
                # 返回的数据进行序列化
                data_unicode = json.loads(response.text)
                self.logger.debug('Response is {}'.format(data_unicode))
                #data_json = response.json()

                if data_unicode == u'remind key':
                    # cookie 到期
                    self.logger.info('get_page response content is remind key retry again')
                    self.sess, self.vl5x = self.get_sess()
                    continue
                elif data_unicode == u'remind':
                    # cookie访问次数过多
                    self.sess, self.vl5x = self.get_sess()
                    ua = random.choice(self.ua_list)
                    remind_captcha = self.sess.get(self.url_list['validate_code_url'], headers=header)
                    img = retrive_img(remind_captcha)
                    img = process_img(img)
                    captcha = recognize(img)
                    captcha_data = {
                        'ValidateCode': captcha
                    }
                    sess.post(self.url_list['check_visit_code_url'], headers=header, data=captcha_data)
                    print('get_first_page response content is remind  retry again')
                    continue
                else:
                    #return data_unicode
                    return data_json
                # 每一页的docID
                id_list = re.findall(u'''.*?"文书ID\\":\\"(.*?)\\",''', data_unicode)
                # count是根据条件condition 筛选出来的总文档数 根据count决定要爬多少页
                data_list = json.loads(data_unicode)
                if len(data_list) == 0:
                    time.sleep(2)
                    print('getFirstPage response content is [] retry again')
                    continue
                count = data_list[0]['Count']
                count = int(count)
                return count, id_list
            except Exception as e:
                print(e)
                i += 1
                if i == 5:
                    #message = anyou + ': ' + str(index) + str(e) + '   ' + 'is bad'
                    #logger.error(message)
                    #print(message)
                    return '', ''


    def get_case_list(self):
        name_list = list()
        date_list = list()
        id_list = list()
        case_id_list = list()
        brief_list = list()
        procedure_list = list()
        court_list = list()
        max_page = self.total_items // self.item_in_page
        if self.total_items % self.item_in_page:
            max_page += 1
        pattern_name = re.compile('"案件名称":"(.*?)"', re.S)
        pattern_id = re.compile('"文书ID":"(.*?)"', re.S)
        pattern_date = re.compile('"裁判日期":"(.*?)"', re.S)
        pattern_case_id = re.compile('"案号":"(.*?)"', re.S)
        pattern_brief = re.compile('"裁判要旨段原文":"(.*?)"', re.S)
        pattern_procedure = re.compile('"审判程序":"(.*?)"', re.S)
        pattern_court = re.compile('"法院名称":"(.*?)"', re.S)
            
        for i in range(1, max_page + 1):
            self.logger.info("Get case list on page {}".format(i))
            raw = self.get_page(i)
            #r = requests.post(self.search_url, headers=self.headers, data=self.data)
            name_list += re.findall(pattern_name, raw)
            id_list += re.findall(pattern_id, raw)
            date_list += re.findall(pattern_date,raw)
            case_id_list += re.findall(pattern_case_id, raw)
            brief_list += re.findall(pattern_brief, raw)
            procedure_list += re.findall(pattern_procedure, raw)
            court_list +=  re.findall(pattern_court, raw)
        self.case_brief['name'] = name_list
        self.case_brief['doc_id'] = id_list
        self.case_brief['date'] = date_list
        self.case_brief['case_id'] = case_id_list
        self.case_brief['brief'] = brief_list
        self.case_brief['procedure'] = procedure_list
        self.case_brief['court'] = court_list
                    
def main():
    pass

    
if __name__ == "__main__":
    main()