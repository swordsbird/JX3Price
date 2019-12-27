blacklist = [
    '月租',
    '已租',
    'W【六合一琴娘7k5】狐金蓝娃娃黄娃娃叽盒红盒青盒粉盒白花朝',
    '执夷白狐、12879海芝【红黑白路秀姐8K】',
    '白无色粉封川雪涛春A2824【绝代秀姐2K】猴',
    '【唯满侠1985417【飞龙12899秀姐     】五红风华',
    '【FL332 飞龙毒姐1999】鸡红，雪月交晖，1商城，95输出大CW等',
    '5397【华乾炮姐】狗红·鸡金飞灵金·黑寒梅蓝望云·烟花套工',
    '菀之Q3278806652←1787【电五剑胆刀娘4W8】六红猴红狐金猴金',
    'H1324【花姐1W4】华乾5红兔金龙女金国金考金鸡金蝶金',
    'PWD1779【电月毒姐1W】100小铁108',
    'A7147【电一龙虎毒姐2W6】',
    'YW5266【双梦道姑6K5】羊红猴红苏金',
    '2063【龙虎秀姐2W2】100级大铁归',
    '1337【3k自定】电五姨妈盾娘',
    'QGM3004号【喵姐1W】95CW残月惊天.鸡猴八红5金发.双',
    '淑SSY267【双一秀姐2淑W2】',
    'MJ1181【电五喵姐2w1】100CW阴阳往极·',
    '195【花姐纵月】猴红蝶金玫瑰金',
    'C8078【电五秀姐8k5】',
    'T1919【长安秀姐】四红',
    'B4232【电五炮姐8800】三山四海',
    'DM3560【双梦伞娘2W5】六红',
    'G422【唯满侠毒姐3W6】五红狐7金粉白菜谷雨蓝娃',
    '苏叶544【七秀成女1w7】猴红九红狐金喵',
    'C9228【电八风骨毒姐5K6】',
    '无色粉封川雪涛春A2824（知遇QQ3106203884）',
    'A7929艾艾【电五毒姐3K6】猴红',
    'L3983 毒姐【2w5】唯满侠 100小铁满',
]

params = {'正太': 0.6871568168259946, '萝莉': 0.7039703936591937, '成男': 0.8986076680312852, '成女': 0.8201792542813118, '红发': 0.3418576507706144, 
          '金发': 0.8799286718934426, '五限': 0.346259676483666, '六限': 0.6669614785771367, '限时': 0.3355914239999999, '复刻': 0.31150079999999997, 
          '挂宠': 0.1204563037768132, '包身盒子': 1.0038022574436896, '普通盒子': 0.6751740487725363, '奇遇': 0.7, '其他': 0.7358173705635102, '统计': 0.31189348937752825,
          '苍云': 0.9377781780739198, '七秀': 0.8875605100399341, '五毒': 0.9270956076568643, '万花': 0.9735355102731975, '藏剑': 0.9149094905391243, '纯阳': 0.9678616362695025,
          '长歌': 0.8828940016600454, '明教': 0.984064187818218, '天策': 0.9834467937303049, '丐帮': 0.8925225347650911, '唐门': 0.9759731017850558, '霸刀': 0.9984009597440255, 
          '凌雪': 2.6296742366970345, '蓬莱': 1.0803540349595513, 'exp': 0.4737103047935288, 'base': 153.88307302459157}

body_penalty = {'正太': 0.7, '萝莉': 0.8, '成男': 1.3, '成女': 1.2}
type_penalty = { '红发': 0.3, '金发': 0.35, '六限': 0.3, '限时': 0.35, '复刻': 0.3, '挂宠': 0.3, '盒子': 0.35, '其他': 1 }
school_penalty = { '凌雪': 2.5, '蓬莱': 1.5 }

random_change_weight = { '红发': 120, '金发': 120, '六限': 120, '限时': 140, '复刻': 140, '挂宠': 160, '盒子': 300 }

fix_pairs = [['红发', ['rhair']], ['金发', ['ghair']], ['五限', ['cl5']], ['六限', ['cl6']], [
    '限时', ['cl7']], ['复刻', ['cln']], ['挂宠', ['pat']], ['盒子', ['box', 'boxn']]]

reserved_items = ['四红', '五红', '六红', '猴红', '羊红', '一代金', '狐金', '猴金', '龙女金', '中秋金', '狗金', '丝路金', '兔金', '考金', '粉繁',
                  '橙繁', '红墨韵', '黑墨韵', '黑风露', '蓝风露', '粉白菜', '紫白菜',
                  '谷雨', '情阅', '白金夜斩白', '黑金夜斩白', '白罗姆', '蓝罗姆', '黑风华', '红彩云', '蓝彩云', '蓝公主', '粉公主', '粉人面', '蓝人面',
                  '绿不欺', '蓝不欺', '白娃娃', '粉娃娃', '黄娃娃', '蓝娃娃', '黑年轮', '红年轮', '黄年轮',
                  '蓝年轮', '白无色',  '黄兰若', '红兰若', '黑兰若', '蓝兰若', '红容与', '绿容与', '紫容与',
                  '粉容与', '黄长安', '绿长安', '红长安', '紫长安', '粉兰亭', '紫兰亭', '黄兰亭', '白兰亭', '白九壤', '黄九壤', '粉九壤', '蓝九壤', '红长天', '绿长天', '蓝长天', '白长天',
                  '红舞步', '粉舞步', '蓝舞步', '黑舞步', '白重天', '粉重天', '黄重天', '黑重天', '蓝天涯', '紫天涯', '黑天涯', '绿天涯',
                  '飒西风陵烟', '飒西风雪回', '飒西风苍璧', '飒西风清江', '飒西风丹壑', '飒西风龙旌', '绿中宵', '黄中宵', '紫中宵', '白中宵',
                  '榆塞裂衿', '榆塞斩芒', '榆塞寒塘', '榆塞振锋', '黑榆塞', '榆塞落旌',
                  '打歌服', '明镜高悬', '富婆套', '复刻繁折风', '复刻繁故幽', '复刻绿白菜', '复刻瓜白菜', '复刻霜降', '复刻惊蛰', '黑夜斩白', '白夜斩白', '复刻粉罗姆',
                  '复刻蓝罗姆', '复刻红紧那', '复刻白策马', '复刻黑策马', '复刻黑彩云',
                  '复刻粉彩云', '复刻黑潇湘', '复刻白潇湘', '复刻蓝天河', '复刻黄天河', '金罗姆', '望月', '情人枕', '六周年龙', '孔雀', '六翼', '特效粉', '金鱼', '狐狸毛', '钰瓣', '天辉', '暗夜',
                  '喵萝干', '狄仁杰黑', '狄仁杰白', '一代黄', '一代白', '一代粉', '一代黑', '一代红', '一代紫', '二代粉',
                  '二代蓝', '二代白', '二代紫', '二代红', '二代黑', '狼头', '黑竹笋', '白莲花', '蓝扇子',
                  '秃盒', '鸡盒', '花盒', '红盒', '飞天盒', '丝路盒', '粉马盒', '黑马盒', '一代重阳盒', '一代七夕盒', '一代中秋蓝', '一代中秋粉', '一代元宵盒', '狄仁杰盒',  '熊猫', '大雕', '复刻',
                  '下架', '五限', '六限', '限时', '限量', '成衣', '奇遇', '红发', '金发', '白发', '黑发', '盒子', '挂宠', '披风', '五甲', '奇趣', '拓印', '脚印', '100小铁', '宠物', '资历']
