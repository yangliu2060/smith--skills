"""
视觉风格模板系统 - Z-Image Skill v1.0

提供 24+ 种预设视觉风格，按系列分组：
- 动漫系列 (anime_*): 日式动漫、Q版萌系、热血少年、治愈系、赛博朋克
- 霓虹系列 (neon_*): 智慧哲理、科技未来、财富投资、对比构图、时间轴、思维导图
- 科技系列 (tech_*): 深蓝科技、浅色商务
- 纪录片系列 (documentary, vintage_*)
- 艺术系列 (watercolor, ink_chinese, comic_style)
- 简约系列 (minimal_white, flat_design)
- 氛围系列 (warm_cozy, dark_dramatic)

默认风格：anime_japanese（日式动漫）
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class StyleCategory(Enum):
    """风格分类"""
    ANIME = "anime"
    NEON = "neon"
    TECH = "tech"
    DOCUMENTARY = "documentary"
    ART = "art"
    MINIMAL = "minimal"
    MOOD = "mood"


@dataclass
class StyleTemplate:
    """视觉风格模板"""
    name: str
    description: str
    base_style: str
    colors: str
    lighting: str
    modifiers: str
    negative: str = ""
    category: StyleCategory = StyleCategory.TECH


# ============================================================
# 风格模板定义 - 24+ 种预设风格
# ============================================================

STYLES: Dict[str, StyleTemplate] = {

    # ========== 动漫系列 (Anime Series) ==========

    "anime_japanese": StyleTemplate(
        name="日式动漫",
        description="经典日本动漫风格，适合故事/角色/冒险类内容",
        base_style="anime illustration, Japanese animation style, cel shading, detailed line art",
        colors="vibrant saturated colors, soft gradients, pastel highlights, anime color palette",
        lighting="dramatic anime lighting, rim light, soft ambient shadows, sakura petals",
        modifiers="expressive characters, dynamic poses, detailed backgrounds, anime aesthetics, studio quality",
        negative="realistic, western cartoon, 3D render, photo, ugly, deformed",
        category=StyleCategory.ANIME
    ),

    "anime_chibi": StyleTemplate(
        name="Q版萌系",
        description="可爱Q版风格，适合轻松/搞笑/日常类内容",
        base_style="chibi style, cute character design, kawaii aesthetic, super deformed",
        colors="bright pastel colors, pink and blue accents, soft candy palette, cheerful tones",
        lighting="flat soft lighting, minimal shadows, bright cheerful atmosphere",
        modifiers="big eyes, small body, adorable expressions, simple background, moe style",
        negative="realistic, dark, horror, detailed anatomy, scary, mature",
        category=StyleCategory.ANIME
    ),

    "anime_shonen": StyleTemplate(
        name="热血少年",
        description="热血战斗风格，适合动作/战斗/励志类内容",
        base_style="shonen anime style, dynamic action illustration, battle manga aesthetic",
        colors="high contrast colors, fiery reds and oranges, electric blues, intense color palette",
        lighting="dramatic backlighting, energy aura effects, explosive light bursts, speed lines",
        modifiers="powerful poses, intense expressions, action lines, dramatic composition, epic scale",
        negative="calm, peaceful, static, realistic, soft, gentle",
        category=StyleCategory.ANIME
    ),

    "anime_iyashikei": StyleTemplate(
        name="治愈系",
        description="治愈系风格，适合温馨/日常/情感类内容",
        base_style="iyashikei anime style, slice of life illustration, soft cozy aesthetic",
        colors="warm muted pastels, soft cream and peach tones, gentle greens, nostalgic palette",
        lighting="golden hour lighting, soft diffused sunlight, warm ambient glow, dreamy atmosphere",
        modifiers="peaceful scenes, gentle expressions, nature elements, comfortable mood, heartwarming",
        negative="action, violence, dark, intense, scary, dramatic",
        category=StyleCategory.ANIME
    ),

    "anime_cyberpunk": StyleTemplate(
        name="赛博朋克动漫",
        description="赛博朋克动漫风格，适合科幻/未来/都市类内容",
        base_style="cyberpunk anime style, futuristic illustration, neon-noir aesthetic",
        colors="neon pink and cyan, deep purple shadows, holographic accents, night city palette",
        lighting="neon signs glow, rain reflections, holographic displays, atmospheric fog",
        modifiers="futuristic cityscape, tech implants, rain-soaked streets, dystopian beauty",
        negative="natural, rural, historical, bright daylight, cheerful",
        category=StyleCategory.ANIME
    ),

    # ========== 霓虹系列 (Neon Series) ==========

    "neon_wisdom": StyleTemplate(
        name="霓虹智慧",
        description="深黑背景+霓虹蓝光效+扁平插画，适合哲理/思考/认知类内容",
        base_style="flat vector illustration, minimalist silhouette art, clean graphic design",
        colors="pure black background #000000, neon cyan glow #00D4FF, electric blue accents, subtle gold highlights #FFD700",
        lighting="neon glow effects, soft light bloom, inner glow on elements, ambient rim lighting",
        modifiers="modern infographic style, abstract metaphor visualization, symbolic imagery, clean composition, professional motion graphics aesthetic",
        negative="realistic photo, detailed textures, cluttered, busy, 3D render, gradients",
        category=StyleCategory.NEON
    ),

    "neon_tech": StyleTemplate(
        name="霓虹科技",
        description="科技感霓虹风格，适合AI/互联网/创业类内容",
        base_style="futuristic vector art, tech illustration, digital aesthetic",
        colors="dark navy background #0a0a1a, neon blue #00D4FF, electric purple #A29BFE, matrix green accents",
        lighting="neon tube lighting, holographic glow, cyberpunk atmosphere, data stream particles",
        modifiers="high-tech, futuristic, digital network, connected nodes, circuit patterns",
        negative="organic, natural, vintage, rustic, hand-drawn",
        category=StyleCategory.NEON
    ),

    "neon_wealth": StyleTemplate(
        name="霓虹财富",
        description="财富主题霓虹风格，适合投资/财务自由/商业类内容",
        base_style="symbolic illustration, wealth metaphor art, infographic style",
        colors="deep black background, glowing gold #FFD700, neon cyan #00D4FF, money green accents #2ECC71",
        lighting="golden glow on wealth symbols, soft ambient light, spotlight on key elements",
        modifiers="financial symbols, growth charts, money tree metaphor, passive income visualization",
        negative="poverty imagery, dark mood, cluttered, realistic money photos",
        category=StyleCategory.NEON
    ),

    "neon_contrast": StyleTemplate(
        name="霓虹对比",
        description="对比构图霓虹风格，适合VS/对比/选择类内容",
        base_style="split composition, comparison layout, diptych style illustration",
        colors="black background, contrasting neon colors left vs right, cyan #00D4FF vs coral #FF6B6B",
        lighting="different lighting moods per side, glow effects, clear visual separation",
        modifiers="versus composition, clear contrast, symbolic comparison, balanced layout",
        negative="unified style, single mood, gradient blend, merged elements",
        category=StyleCategory.NEON
    ),

    "neon_timeline": StyleTemplate(
        name="霓虹时间轴",
        description="时间轴叙事霓虹风格，适合人物传记/发展历程类内容",
        base_style="timeline infographic, journey visualization, progression art",
        colors="dark background, glowing path line #00D4FF, milestone markers in gold #FFD700, year labels in white",
        lighting="glowing timeline path, spotlight on milestones, particle trail effect",
        modifiers="horizontal timeline, growth progression, seed to tree metaphor, year markers",
        negative="static, no progression, cluttered timeline, realistic photos",
        category=StyleCategory.NEON
    ),

    "neon_mindmap": StyleTemplate(
        name="霓虹思维导图",
        description="思维导图霓虹风格，适合总结/知识结构/框架类内容",
        base_style="radial mind map, concept network, knowledge graph visualization",
        colors="black background, central node gold #FFD700, branches cyan #00D4FF, sub-nodes purple #A29BFE",
        lighting="glowing nodes, connection lines with glow, radial light spread",
        modifiers="central concept, radiating branches, hierarchical structure, clean connections",
        negative="linear layout, cluttered, overlapping, realistic",
        category=StyleCategory.NEON
    ),

    # ========== 科技系列 (Tech Series) ==========

    "tech_dark": StyleTemplate(
        name="科技深蓝",
        description="深蓝背景、青色发光、科技感，适合商业/科技类内容",
        base_style="minimalist illustration, clean vector art, tech style",
        colors="dark blue background, cyan glow effects, neon accents",
        lighting="soft ambient lighting, subtle gradients, glowing elements",
        modifiers="modern, sleek, professional, futuristic",
        negative="realistic photo, cluttered, messy, bright colors",
        category=StyleCategory.TECH
    ),

    "tech_light": StyleTemplate(
        name="科技浅色",
        description="浅色背景、蓝色调、干净现代，适合产品展示",
        base_style="minimalist design, clean lines, modern aesthetic",
        colors="light gray background, blue accents, white space",
        lighting="bright even lighting, soft shadows",
        modifiers="clean, minimal, professional, contemporary",
        negative="dark, gloomy, cluttered, vintage",
        category=StyleCategory.TECH
    ),

    # ========== 纪录片系列 (Documentary Series) ==========

    "documentary": StyleTemplate(
        name="纪录片风格",
        description="电影级质感、真实感、适合人物传记",
        base_style="cinematic photography, documentary style, photorealistic",
        colors="muted tones, natural colors, film grain",
        lighting="cinematic lighting, dramatic shadows, golden hour",
        modifiers="authentic, emotional, storytelling, atmospheric",
        negative="cartoon, anime, illustration, oversaturated",
        category=StyleCategory.DOCUMENTARY
    ),

    "vintage_50s": StyleTemplate(
        name="50年代复古",
        description="1950年代美国风格，适合历史类内容",
        base_style="vintage photography, 1950s America, retro aesthetic",
        colors="sepia tones, faded colors, warm vintage palette",
        lighting="soft natural light, nostalgic atmosphere",
        modifiers="historical, authentic, period-accurate, nostalgic",
        negative="modern, digital, neon, futuristic",
        category=StyleCategory.DOCUMENTARY
    ),

    "vintage_80s": StyleTemplate(
        name="80年代复古",
        description="1980年代风格，霓虹、合成波",
        base_style="synthwave aesthetic, 80s retro, neon style",
        colors="pink and purple neon, chrome reflections, sunset gradients",
        lighting="neon glow, laser lights, dramatic contrast",
        modifiers="retro futuristic, vaporwave, outrun style",
        negative="natural, organic, muted, minimal",
        category=StyleCategory.DOCUMENTARY
    ),

    # ========== 艺术系列 (Art Series) ==========

    "watercolor": StyleTemplate(
        name="水彩画风",
        description="柔和水彩效果，适合情感类内容",
        base_style="watercolor painting, soft edges, artistic",
        colors="pastel colors, soft gradients, transparent washes",
        lighting="diffused light, dreamy atmosphere",
        modifiers="artistic, emotional, delicate, flowing",
        negative="sharp edges, photorealistic, digital, harsh",
        category=StyleCategory.ART
    ),

    "ink_chinese": StyleTemplate(
        name="中国水墨",
        description="传统中国水墨画风格",
        base_style="Chinese ink painting, sumi-e style, brush strokes",
        colors="black ink, white space, minimal red accents",
        lighting="atmospheric, misty, ethereal",
        modifiers="traditional, zen, minimalist, elegant",
        negative="colorful, modern, digital, western",
        category=StyleCategory.ART
    ),

    "comic_style": StyleTemplate(
        name="美式漫画",
        description="美式漫画风格，适合娱乐类内容",
        base_style="comic book style, bold outlines, cel shading",
        colors="vibrant primary colors, halftone dots, bold contrast",
        lighting="flat lighting, strong shadows, dramatic",
        modifiers="dynamic, action, expressive, pop art",
        negative="realistic, muted, subtle, photographic",
        category=StyleCategory.ART
    ),

    # ========== 简约系列 (Minimal Series) ==========

    "minimal_white": StyleTemplate(
        name="极简白色",
        description="极简主义、大量留白",
        base_style="minimalist design, negative space, clean",
        colors="white background, subtle gray accents, monochrome",
        lighting="bright, even, shadowless",
        modifiers="elegant, refined, sophisticated, modern",
        negative="busy, colorful, detailed, cluttered",
        category=StyleCategory.MINIMAL
    ),

    "flat_design": StyleTemplate(
        name="扁平设计",
        description="扁平化设计风格，适合解释类视频",
        base_style="flat design, vector illustration, 2D graphics",
        colors="solid colors, no gradients, limited palette",
        lighting="no shadows, flat, uniform",
        modifiers="simple, clear, modern, infographic style",
        negative="3D, realistic, shadows, textures",
        category=StyleCategory.MINIMAL
    ),

    # ========== 氛围系列 (Mood Series) ==========

    "warm_cozy": StyleTemplate(
        name="温暖舒适",
        description="温暖色调、舒适氛围，适合家庭/生活类",
        base_style="cozy atmosphere, warm tones, inviting",
        colors="warm orange and yellow, soft browns, golden hues",
        lighting="warm golden light, soft shadows, candlelight feel",
        modifiers="comfortable, homey, intimate, welcoming",
        negative="cold, harsh, clinical, sterile",
        category=StyleCategory.MOOD
    ),

    "dark_dramatic": StyleTemplate(
        name="暗黑戏剧",
        description="高对比、戏剧化，适合悬疑/冲突类",
        base_style="dramatic noir, high contrast, cinematic",
        colors="deep blacks, stark whites, minimal color",
        lighting="chiaroscuro, dramatic shadows, spotlight",
        modifiers="intense, mysterious, powerful, theatrical",
        negative="bright, cheerful, colorful, flat",
        category=StyleCategory.MOOD
    ),
}


# ============================================================
# 默认风格配置
# ============================================================

DEFAULT_STYLE = "anime_japanese"


# ============================================================
# 风格检测器（Detector Chain）
# ============================================================

def detect_anime_style(text: str) -> Optional[str]:
    text_lower = text.lower()
    cyberpunk_keywords = ["赛博朋克", "cyberpunk", "未来都市", "黑客", "机械", "义体", "霓虹都市"]
    if any(kw in text_lower for kw in cyberpunk_keywords):
        return "anime_cyberpunk"
    shonen_keywords = ["战斗", "热血", "战争", "冒险", "英雄", "battle", "fight", "hero", "龙珠", "海贼", "火影"]
    if any(kw in text_lower for kw in shonen_keywords):
        return "anime_shonen"
    chibi_keywords = ["可爱", "萌", "搞笑", "日常", "chibi", "cute", "kawaii", "Q版", "轻松"]
    if any(kw in text_lower for kw in chibi_keywords):
        return "anime_chibi"
    iyashikei_keywords = ["治愈", "温馨", "日常", "peaceful", "relaxing", "夏目", "轻音", "暖心"]
    if any(kw in text_lower for kw in iyashikei_keywords):
        return "anime_iyashikei"
    anime_keywords = ["动漫", "动画", "番剧", "二次元", "anime", "漫画", "轻小说", "异世界", "isekai"]
    if any(kw in text_lower for kw in anime_keywords):
        return "anime_japanese"
    return None


def detect_neon_style(text: str) -> Optional[str]:
    text_lower = text.lower()
    wealth_keywords = ["财富", "金钱", "投资", "被动收入", "财务自由", "资产", "复利", "杠杆", "wealth", "money", "passive income"]
    if any(kw in text_lower for kw in wealth_keywords):
        return "neon_wealth"
    wisdom_keywords = ["智慧", "哲学", "人生", "幸福", "纳瓦尔", "naval", "思维", "认知", "philosophy", "wisdom", "happiness"]
    if any(kw in text_lower for kw in wisdom_keywords):
        return "neon_wisdom"
    tech_keywords = ["ai", "人工智能", "科技", "互联网", "创业", "技术", "代码", "软件", "tech", "startup", "code"]
    if any(kw in text_lower for kw in tech_keywords):
        return "neon_tech"
    contrast_keywords = ["vs", "对比", "区别", "比较", "versus", "对立", "差异"]
    if any(kw in text_lower for kw in contrast_keywords):
        return "neon_contrast"
    timeline_keywords = ["时间轴", "历程", "发展", "成长", "阶段", "timeline", "journey", "evolution"]
    if any(kw in text_lower for kw in timeline_keywords):
        return "neon_timeline"
    mindmap_keywords = ["总结", "框架", "核心", "要点", "知识", "summary", "framework", "key points"]
    if any(kw in text_lower for kw in mindmap_keywords):
        return "neon_mindmap"
    return None


def detect_documentary_style(text: str) -> Optional[str]:
    text_lower = text.lower()
    eighties_keywords = ["80年代", "1980", "复古", "synthwave", "vaporwave", "合成波"]
    if any(kw in text_lower for kw in eighties_keywords):
        return "vintage_80s"
    fifties_keywords = ["50年代", "1950", "美国梦", "黄金时代", "老电影"]
    if any(kw in text_lower for kw in fifties_keywords):
        return "vintage_50s"
    documentary_keywords = ["纪录片", "传记", "documentary", "真实故事", "历史", "biography"]
    if any(kw in text_lower for kw in documentary_keywords):
        return "documentary"
    return None


def detect_art_style(text: str) -> Optional[str]:
    text_lower = text.lower()
    ink_keywords = ["水墨", "国画", "禅", "zen", "中国风", "传统", "书法"]
    if any(kw in text_lower for kw in ink_keywords):
        return "ink_chinese"
    watercolor_keywords = ["水彩", "watercolor", "柔和", "梦幻", "诗意"]
    if any(kw in text_lower for kw in watercolor_keywords):
        return "watercolor"
    comic_keywords = ["漫威", "dc", "美漫", "comic", "超级英雄"]
    if any(kw in text_lower for kw in comic_keywords):
        return "comic_style"
    return None


def detect_mood_style(text: str) -> Optional[str]:
    text_lower = text.lower()
    dark_keywords = ["悬疑", "恐怖", "黑暗", "noir", "thriller", "惊悚", "神秘"]
    if any(kw in text_lower for kw in dark_keywords):
        return "dark_dramatic"
    warm_keywords = ["温馨", "家庭", "舒适", "cozy", "温暖", "幸福家庭"]
    if any(kw in text_lower for kw in warm_keywords):
        return "warm_cozy"
    return None


def detect_scene_style(text: str) -> Optional[str]:
    """
    场景感知检测器 — 根据画面内容（而非内容主题）选择风格

    优先级最高，在所有内容类型检测器之前运行。
    解决"野猫躺在雪地里"被错误分配到 anime_japanese 的问题。
    """
    text_lower = text.lower()

    # 中国古风/武侠/仙侠 → 水墨
    chinese_scene = ["古风", "武侠", "仙侠", "江湖", "侠客", "剑客", "道士", "仙人",
                     "古装", "汉服", "唐装", "宫殿", "庙宇", "亭台", "楼阁", "山水画"]
    if any(kw in text_lower for kw in chinese_scene):
        return "ink_chinese"

    # 自然风景/动物/户外 → 纪录片写实
    nature_scene = ["雪地", "雪景", "森林", "山脉", "大海", "海洋", "沙漠", "草原", "湖泊",
                    "河流", "瀑布", "日落", "日出", "星空", "极光", "雨林", "冰川",
                    "野猫", "老虎", "狮子", "鹰", "鹿", "狼", "熊", "鲸鱼", "海豚",
                    "野生动物", "自然", "荒野", "田野", "花海", "樱花", "雪山",
                    "snow", "forest", "ocean", "mountain", "wildlife", "nature",
                    "cat in", "dog in", "animal", "landscape", "sunset", "sunrise"]
    if any(kw in text_lower for kw in nature_scene):
        return "documentary"

    # 都市/街景/建筑 → 科技深蓝
    urban_scene = ["城市", "都市", "摩天大楼", "街道", "夜景", "天际线", "地铁",
                   "city", "urban", "skyline", "skyscraper", "street", "downtown"]
    if any(kw in text_lower for kw in urban_scene):
        return "tech_dark"

    # 美食/食物 → 温暖舒适
    food_scene = ["美食", "食物", "料理", "蛋糕", "咖啡", "餐厅", "厨房",
                  "拉面", "寿司", "火锅", "烧烤", "甜点", "面包", "饺子", "汤",
                  "food", "cuisine", "cake", "coffee", "restaurant", "cooking",
                  "noodle", "sushi", "pizza", "dessert", "bread"]
    if any(kw in text_lower for kw in food_scene):
        return "warm_cozy"

    # 人像/肖像 → 纪录片写实
    portrait_scene = ["肖像", "人像", "面部", "眼神", "表情", "老人", "少女", "孩子",
                      "portrait", "face", "expression", "close-up of person"]
    if any(kw in text_lower for kw in portrait_scene):
        return "documentary"

    # 梦幻/诗意/情感 → 水彩
    dreamy_scene = ["梦境", "幻想", "童话", "仙境", "花园", "蝴蝶", "萤火虫",
                    "dream", "fantasy", "fairy", "garden", "butterfly", "firefly",
                    "诗意", "浪漫", "唯美"]
    if any(kw in text_lower for kw in dreamy_scene):
        return "watercolor"

    return None


# ============================================================
# 主检测函数
# ============================================================

def auto_detect_style(topic: str, content: str = "", use_llm: bool = True, model: Optional[str] = None) -> str:
    """
    自动检测最佳风格

    优先使用 LLM 智能判断，降级到关键词匹配。

    Args:
        topic: 主题
        content: 可选内容文本
        use_llm: 是否使用 LLM（默认 True）
        model: 指定 LLM 模型

    Returns:
        推荐的风格名称
    """
    full_text = f"{topic} {content}"

    if use_llm:
        llm_result = _detect_style_with_llm(full_text, model=model)
        if llm_result:
            return llm_result

    return _detect_style_with_keywords(full_text)


def _detect_style_with_keywords(text: str) -> str:
    """关键词匹配检测风格（降级方案）"""
    detectors = [
        detect_scene_style,       # 场景感知（最高优先级）
        detect_anime_style,
        detect_neon_style,
        detect_documentary_style,
        detect_art_style,
        detect_mood_style,
    ]
    for detector in detectors:
        result = detector(text)
        if result:
            return result
    return DEFAULT_STYLE


def _detect_style_with_llm(text: str, model: Optional[str] = None) -> Optional[str]:
    """使用 LLM 智能判断最佳风格"""
    import logging
    logger = logging.getLogger(__name__)

    try:
        import anthropic
        import os

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            logger.debug("ANTHROPIC_API_KEY 未设置，降级到关键词匹配")
            return None

        client = anthropic.Anthropic(api_key=api_key)

        if model is None:
            model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

        style_options = "\n".join([
            f"- {style_id}: {style.name} - {style.description}"
            for style_id, style in STYLES.items()
        ])

        prompt = f"""请根据以下内容，选择最合适的视觉风格。

## 内容：
{text}

## 可用风格：
{style_options}

请只返回风格ID（如 anime_japanese），不要返回其他内容。"""

        response = client.messages.create(
            model=model,
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.content[0].text.strip().lower()

        if result in STYLES:
            logger.info(f"LLM 推荐风格: {result}")
            return result
        else:
            logger.warning(f"LLM 返回无效风格: {result}")
            return None

    except ImportError:
        logger.debug("anthropic 库未安装，降级到关键词匹配")
        return None
    except Exception as e:
        logger.warning(f"LLM 风格检测失败: {e}")
        return None


# ============================================================
# 公共 API
# ============================================================

def get_style_prompt(prompt: str, style: str = DEFAULT_STYLE, include_negative: bool = True) -> str:
    """
    用风格模板增强 prompt

    Args:
        prompt: 原始 prompt
        style: 风格 ID
        include_negative: 是否包含 negative prompt

    Returns:
        增强后的 prompt（如果 include_negative=True，用 ||| 分隔正负 prompt）
    """
    template = STYLES.get(style)
    if not template:
        template = STYLES[DEFAULT_STYLE]

    enhanced = f"{prompt}, {template.base_style}, {template.colors}, {template.lighting}, {template.modifiers}"

    if include_negative and template.negative:
        return f"{enhanced} ||| {template.negative}"
    return enhanced


def get_style_for_content(content_type: str) -> str:
    """根据内容类型推荐风格"""
    content_map = {
        "tech": "tech_dark",
        "business": "neon_tech",
        "philosophy": "neon_wisdom",
        "wealth": "neon_wealth",
        "anime": "anime_japanese",
        "action": "anime_shonen",
        "cute": "anime_chibi",
        "healing": "anime_iyashikei",
        "cyberpunk": "anime_cyberpunk",
        "documentary": "documentary",
        "art": "watercolor",
        "chinese": "ink_chinese",
        "minimal": "minimal_white",
        "dark": "dark_dramatic",
        "warm": "warm_cozy",
        "comparison": "neon_contrast",
        "timeline": "neon_timeline",
        "summary": "neon_mindmap",
    }
    return content_map.get(content_type, DEFAULT_STYLE)


def list_styles() -> List[Dict]:
    """列出所有风格"""
    return [
        {"id": sid, "name": s.name, "description": s.description, "category": s.category.value}
        for sid, s in STYLES.items()
    ]


def list_styles_by_category(category: str) -> List[Dict]:
    """按分类列出风格"""
    try:
        cat = StyleCategory(category)
    except ValueError:
        return []
    return [
        {"id": sid, "name": s.name, "description": s.description}
        for sid, s in STYLES.items()
        if s.category == cat
    ]


if __name__ == "__main__":
    print(f"Z-Image Style Templates: {len(STYLES)} styles in {len(StyleCategory)} categories\n")
    for cat in StyleCategory:
        styles = list_styles_by_category(cat.value)
        print(f"[{cat.value}] ({len(styles)} styles)")
        for s in styles:
            print(f"  - {s['id']}: {s['name']} - {s['description']}")
        print()
