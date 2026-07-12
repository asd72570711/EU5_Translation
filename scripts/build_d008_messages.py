#!/usr/bin/env python3
"""Build the repetitive D008 action-message translation JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path

SOURCE = Path("source/english/main_menu/localization/english/dlc/d008_fate_of_the_phoenix/D008_messages_l_english.yml")
OUTPUT = Path("work/translations/D008_messages_l_english.json")
LINE_RE = re.compile(r'^\s*(?P<key>[^:#][^:]*):\s*"(?P<value>.*)"\s*$')
TOKEN_RE = re.compile(r"\[[^\]]+\]|\$[^$]+\$|#!|#[A-Za-z_][A-Za-z0-9_]*")

PHRASES = [
    ("When we ", "當我們"),
    ("When another [country|e] ", "當另一個[country|e]"),
    ("When a [country|e] ", "當某個[country|e]"),
    (" have decided to ", "決定"),
    (" has decided to ", "已決定"),
    (" have reestablished ", "已重新建立"),
    (" has reestablished ", "已重新建立"),
    (" have approached us with an offer", "向我們提出提議"),
    (" has appealed to the ", "已向"),
    (" for financial support", "請求財政支援"),
    (" has granted privileges to Italian merchants", "已授予義大利商人特權"),
    (" has received a $catholic$ delegation", "已接待$catholic$使團"),
    (" has attracted an $italian_group$ engineer to their service", "已吸引$italian_group$工程師為其效力"),
    (" has demanded tribute from a Beylik", "已向貝伊國要求貢賦"),
    ("demands tribute from a Beylik", "向貝伊國要求貢賦"),
    ("summons a member of the Autocephalous Patriarchate", "召集自主教會牧首區成員"),
    ("attempts to mend the Religious Schism", "嘗試彌合宗教大分裂"),
    ("attempt to mend the Religious Schism", "嘗試彌合宗教大分裂"),
    ("Mending of the Schism!", "彌合大分裂！"),
    ("Urbs Restituta", "復興之城"),
    ("Olympiad", "奧林匹亞賽會"),
    (" has called upon a member of their ", "已向其"),
    (" for aid", "求援"),
    (" has begun reforming its imperial armies", "已開始改革帝國軍隊"),
    (" has patronized an $orthodox_monastery$", "已資助$orthodox_monastery$"),
    (" has hosted an Olympiad.", "已舉辦奧林匹亞賽會。"),
    ("a [ShowReligionAdjective('hellenism_religion')] [country|e] uses the [ShowGenericActionName('host_olympiad')] action.", "信奉[ShowReligionAdjective('hellenism_religion')]的[country|e]使用[ShowGenericActionName('host_olympiad')]行動。"),
    ("attracts an $italian_group$ military engineer during the", "在……期間吸引$italian_group$軍事工程師"),
    ("demands tribute from a Beylik during the", "在……期間向貝伊國要求貢賦"),
    ("summons a member of the Autocephalous Patriarchate during the", "在……期間召集自主教會牧首區成員"),
    ("decided to exert our influence in the Pentarchy to mend the scars that divide", "決定在五大牧首區發揮影響力，彌合分裂"),
    ("decided to exert their influence in the Pentarchy to mend the scars that divide", "決定在五大牧首區發揮影響力，彌合分裂"),
    ("restore the primacy of", "恢復"),
    (" has used [ShowGenericActionName(", "已使用[ShowGenericActionName("),
    ("When we offer to loan an Icon.", "當我們提出出借聖像。"),
    ("When another [country|e] offers to loan an Icon.", "當另一個[country|e]提出出借聖像。"),
    ("When another [country|e] offers to loan an [icon|e].", "當另一個[country|e]提出出借[icon|e]。"),
    ("When we attempt to mend the Religious Schism.", "當我們嘗試彌合宗教分裂。"),
    ("When another [country|e] attempts to mend the Religious Schism.", "當另一個[country|e]嘗試彌合宗教分裂。"),
    ("When we restore the primacy of ", "當我們恢復"),
    ("When another [country|e] restores the primacy of ", "當另一個[country|e]恢復"),
    ("When we reestablish ", "當我們重新建立"),
    ("When another [country|e] reestablishes ", "當另一個[country|e]重新建立"),
    ("The [SCOPE.sCountry('actor').GetLongName] have decided to ", "[SCOPE.sCountry('actor').GetLongName]已決定"),
    ("The [SCOPE.sCountry('actor').GetLongName] decided to ", "[SCOPE.sCountry('actor').GetLongName]決定"),
    ("[SCOPE.sCountry('actor').GetName] have decided to ", "[SCOPE.sCountry('actor').GetName]已決定"),
    ("[SCOPE.sCountry('actor').GetName] decided to ", "[SCOPE.sCountry('actor').GetName]決定"),
    ("We have decided to ", "我們決定"),
    ("We decided to ", "我們決定"),
    ("We have reestablished ", "我們已重新建立"),
    ("We are brothers in the faith!", "我們是信仰上的兄弟！"),
    ("Icon Loan Offer!", "聖像出借提議！"),
    ("Mending of the Schism!", "彌合分裂！"),
    ("Primacy Restored!", "首要地位恢復！"),
    ("Reestablished!", "重新建立！"),
    ("The [SCOPE.sCountry('actor').GetLongName] have ", "[SCOPE.sCountry('actor').GetLongName]已"),
    (" have decided to offer the loan of ", "已決定出借"),
    (" decided to offer the loan of ", "決定出借"),
    (" to ", "予"),
    ("We will", "我們將"),
    ("When ", "當"),
]

def translate(key: str, value: str) -> str:
    if key.endswith("_HEADER"):
        return "$MESSENGER$"
    if value == "$EFFECT$":
        return "$EFFECT$"
    if key.endswith("_BTN1") or key.endswith("_BTN2"):
        return "確定"
    if key.endswith("_BTN3"):
        return "$common_string_go_to$"
    if key.endswith("_MAP"):
        return ""
    protected: list[str] = []

    def mask(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"__SAFE_{len(protected) - 1}__"

    result = TOKEN_RE.sub(mask, value)
    for old, new in PHRASES:
        result = result.replace(old, new)
    result = result.replace("When a ", "當某個")
    result = result.replace("When another ", "當另一個")
    result = result.replace("The benefits", "這些效益")
    result = result.replace("The ", "")
    result = result.replace(" have ", "有")
    result = result.replace(" has ", "已")
    result = result.replace(" offers ", "提出")
    result = result.replace(" decided ", "決定")
    result = result.replace(" offer ", "提供")
    result = result.replace("We ", "我們")
    result = result.replace("When", "當")
    result = result.replace("OK", "確定")
    result = result.replace("financial support", "財政支援")
    result = result.replace("Italian merchants", "義大利商人")
    result = result.replace("military engineer", "軍事工程師")
    result = result.replace("tribute", "貢賦")
    result = result.replace("Religious Schism", "宗教分裂")
    result = result.replace("the Schism", "大分裂")
    result = result.replace("attempts to mend", "嘗試彌合")
    result = result.replace("attempt to mend", "嘗試彌合")
    result = result.replace("exert our influence", "發揮我們的影響力")
    result = result.replace("their influence", "其影響力")
    result = result.replace("mend the scars that divide", "彌合分裂[ShowReligionGroupName('christian')]的傷痕")
    result = result.replace("Pentarchy", "五大牧首區")
    result = result.replace("original capital of the Empire", "帝國最初的首都")
    result = result.replace("brothers in the faith", "信仰上的兄弟")
    result = result.replace("The scars that divide", "分裂的傷痕")
    result = result.replace("offer the loan", "提出出借")
    result = result.replace("loan of", "出借")
    result = result.replace("Beylik", "貝伊國")
    result = result.replace("Autocephalous Patriarchate", "自主教會牧首區")
    result = result.replace("has", "已")
    result = result.replace("When", "當")
    result = result.replace(" during the ", "期間")
    result = result.replace("during the ", "期間")
    result = result.replace(" in the ", "在")
    result = result.replace(" the ", "")
    result = result.replace(" of ", "的")
    result = re.sub(r" +", " ", result).strip()

    for index, token in enumerate(protected):
        result = result.replace(f"__SAFE_{index}__", token)

    specials = {
        "PERFORM_request_papal_donation_ACTION_SETUP": "當某個[country|e]向[GetCountry('PAP').GetLongNameWithNoTooltip]請求捐款",
        "PERFORM_grant_latin_merchants_privileges_ACTION_SETUP": "當某個[country|e]在[ShowDisasterName('fate_of_the_phoenix')]期間授予義大利商人特權",
        "PERFORM_accept_catholic_delegation_ACTION_SETUP": "當某個[country|e]在[ShowDisasterName('fate_of_the_phoenix')]期間接待$catholic$使團",
        "PERFORM_attract_italian_engineer_ACTION_TITLE": "[SCOPE.sCountry('actor').GetName]已吸引$italian_group$工程師為其效力",
        "PERFORM_accept_catholic_delegation_ACTION_TITLE": "[SCOPE.sCountry('actor').GetName]已接待$catholic$使團",
        "PERFORM_reform_imperial_armies_ACTION_SETUP": "當某個[country|e]在[ShowDisasterName('fate_of_the_phoenix')]期間改革其武裝力量",
        "PERFORM_patronize_orthodox_monastery_ACTION_SETUP": "當某個[country|e]在[ShowDisasterName('fate_of_the_phoenix')]期間資助$orthodox$修道院",
        "PERFORM_patronize_orthodox_monastery_ACTION_TITLE": "[SCOPE.sCountry('actor').GetName]已資助$orthodox_monastery$",
        "PERFORM_host_olympiad_ACTION_SETUP": "當信奉[ShowReligionAdjective('hellenism_religion')]的[country|e]使用[ShowGenericActionName('host_olympiad')]行動。",
        "PERFORM_sponsor_troop_feast_ACTION_SETUP": "當信奉[ShowReligionAdjective('hellenism_religion')]的[country|e]使用[ShowGenericActionName('sponsor_troop_feast')]行動。",
        "PERFORM_sponsor_troop_feast_ACTION_TITLE": "[SCOPE.sCountry('actor').GetName]已使用[ShowGenericActionName('sponsor_troop_feast')]",
        "PERFORM_grant_a_triumph_ACTION_SETUP": "當信奉[ShowReligionAdjective('hellenism_religion')]的[country|e]使用[ShowGenericActionName('grant_a_triumph')]行動。",
        "PERFORM_grant_a_triumph_ACTION_TITLE": "[SCOPE.sCountry('actor').GetName]已使用[ShowGenericActionName('grant_a_triumph')]",
        "PERFORM_roman_festivals_ACTION_SETUP": "當信奉[ShowReligionAdjective('hellenism_religion')]的[country|e]使用[ShowGenericActionName('roman_festivals')]行動。",
        "PERFORM_roman_festivals_ACTION_TITLE": "[SCOPE.sCountry('actor').GetName]已使用[ShowGenericActionName('roman_festivals')]",
        "PERFORM_greek_festivals_ACTION_SETUP": "當信奉[ShowReligionAdjective('hellenism_religion')]的[country|e]使用[ShowGenericActionName('greek_festivals')]行動。",
        "PERFORM_greek_festivals_ACTION_TITLE": "[SCOPE.sCountry('actor').GetName]已使用[ShowGenericActionName('greek_festivals')]",
        "WE_PERFORM_loan_icon_ACTION_SETUP": "當我們提出出借聖像。",
        "OTHER_PERFORMS_loan_icon_ACTION_SETUP": "當另一個[country|e]提出出借聖像。",
        "ACTION_loan_icon_PERFORMED_ON_US_SETUP": "當另一個[country|e]提出出借[icon|e]。",
        "WE_PERFORM_loan_icon_ACTION_LOG": "我們決定將[SCOPE.sWorkOfArt('target').GetName]出借予[SCOPE.sCountry('target_country').GetName]。",
        "OTHER_PERFORMS_loan_icon_ACTION_LOG": "[SCOPE.sCountry('actor').GetLongName]決定將[SCOPE.sWorkOfArt('target').GetName]出借予[SCOPE.sCountry('target_country').GetName]。",
        "ACTION_loan_icon_PERFORMED_ON_US_DESC": "[SCOPE.sCountry('actor').GetName]決定將[SCOPE.sWorkOfArt('target').GetName]出借予[SCOPE.sCountry('target_country').GetName]。",
        "ACTION_loan_icon_PERFORMED_ON_US_LOG": "[SCOPE.sCountry('actor').GetName]決定將[SCOPE.sWorkOfArt('target').GetName]出借予[SCOPE.sCountry('target_country').GetName]。",
        "WE_PERFORM_reestablish_hellenism_ACTION_SETUP": "當我們重新建立[ShowReligionName('hellenism_religion')]。",
        "OTHER_PERFORMS_reestablish_hellenism_ACTION_SETUP": "當另一個[country|e]重新建立[ShowReligionName('hellenism_religion')]。",
        "WE_PERFORM_reestablish_hellenism_ACTION_LOG": "我們已重新建立[ShowReligionName('hellenism_religion')]。",
        "OTHER_PERFORMS_reestablish_hellenism_ACTION_LOG": "[SCOPE.sCountry('actor').GetName]已重新建立[ShowReligionName('hellenism_religion')]。",
        "PERFORM_attract_italian_engineer_ACTION_SETUP": "當某個[country|e]在[ShowDisasterName('fate_of_the_phoenix')]期間吸引$italian_group$軍事工程師",
        "PERFORM_demand_beylik_tribute_ACTION_SETUP": "當某個[country|e]在[ShowDisasterName('fate_of_the_phoenix')]期間向貝伊國要求貢賦",
        "PERFORM_summon_patriarchate_member_ACTION_SETUP": "當某個[country|e]在[ShowDisasterName('fate_of_the_phoenix')]期間召集自主教會牧首區成員",
        "PERFORM_host_olympiad_ACTION_TITLE": "[SCOPE.sCountry('actor').GetName]已舉辦奧林匹亞賽會。",
        "WE_PERFORM_mend_schism_ACTION_SETUP": "當我們嘗試彌合宗教大分裂。",
        "OTHER_PERFORMS_mend_schism_ACTION_SETUP": "當另一個[country|e]嘗試彌合宗教大分裂。",
        "WE_PERFORM_mend_schism_ACTION_TITLE": "彌合大分裂！",
        "OTHER_PERFORMS_mend_schism_ACTION_TITLE": "彌合大分裂！",
        "WE_PERFORM_mend_schism_ACTION_LOG": "我們決定在五大牧首區發揮影響力，彌合分裂[ShowReligionGroupName('christian')]的傷痕。",
        "OTHER_PERFORMS_mend_schism_ACTION_LOG": "[SCOPE.sCountry('actor').GetLongName]決定在五大牧首區發揮影響力，彌合分裂[ShowReligionGroupName('christian')]的傷痕。",
        "WE_PERFORM_restore_rome_primacy_ACTION_SETUP": "當我們恢復[ShowLocationName('rome')]的首要地位。",
        "OTHER_PERFORMS_restore_rome_primacy_ACTION_SETUP": "當另一個[country|e]恢復[ShowLocationName('rome')]的首要地位。",
        "WE_PERFORM_restore_rome_primacy_ACTION_TITLE": "[ShowLocationName('rome')]首要地位恢復！",
        "OTHER_PERFORMS_restore_rome_primacy_ACTION_TITLE": "#italic 復興之城#!!",
        "WE_PERFORM_restore_rome_primacy_ACTION_DESC": "#italic 復興之城#!!",
        "OTHER_PERFORMS_restore_rome_primacy_ACTION_DESC": "#italic 復興之城#!!",
        "WE_PERFORM_restore_rome_primacy_ACTION_LOG": "我們決定恢復[ShowLocationName('rome')]作為帝國最初的首都。",
        "OTHER_PERFORMS_restore_rome_primacy_ACTION_LOG": "[SCOPE.sCountry('actor').GetLongName]決定恢復[ShowLocationName('rome')]作為帝國最初的首都。",
        "WE_PERFORM_reestablish_hellenism_ACTION_TITLE": "[ShowReligionNameWithNoTooltip('hellenism_religion')]重新建立！",
        "OTHER_PERFORMS_reestablish_hellenism_ACTION_TITLE": "[ShowReligionNameWithNoTooltip('hellenism_religion')]重新建立！",
        "WE_PERFORM_reestablish_hellenism_ACTION_DESC": "#italic 復興之城#!!",
        "OTHER_PERFORMS_reestablish_hellenism_ACTION_DESC": "#italic 復興之城#!!",
        "WE_PERFORM_loan_icon_ACTION_EFFECTS": "我們決定將[SCOPE.sWorkOfArt('target').GetName]出借予[SCOPE.sCountry('target_country').GetName]。",
        "OTHER_PERFORMS_loan_icon_ACTION_EFFECTS": "[SCOPE.sCountry('actor').GetLongName]決定將[SCOPE.sWorkOfArt('target').GetName]出借予[SCOPE.sCountry('target_country').GetName]。",
        "WE_PERFORM_mend_schism_ACTION_EFFECTS": "我們決定在五大牧首區發揮影響力，彌合分裂[ShowReligionGroupName('christian')]的傷痕。",
        "OTHER_PERFORMS_mend_schism_ACTION_EFFECTS": "[SCOPE.sCountry('actor').GetLongName]決定在五大牧首區發揮影響力，彌合分裂[ShowReligionGroupName('christian')]的傷痕。",
        "WE_PERFORM_restore_rome_primacy_ACTION_EFFECTS": "我們決定恢復[ShowLocationName('rome')]作為帝國最初的首都。",
        "OTHER_PERFORMS_restore_rome_primacy_ACTION_EFFECTS": "[SCOPE.sCountry('actor').GetLongName]決定恢復[ShowLocationName('rome')]作為帝國最初的首都。",
        "WE_PERFORM_reestablish_hellenism_ACTION_EFFECTS": "我們決定重新建立[ShowReligionAdjective('hellenism_religion')][religion|e]。",
        "OTHER_PERFORMS_reestablish_hellenism_ACTION_EFFECTS": "[SCOPE.sCountry('actor').GetLongName]決定重新建立[ShowReligionAdjective('hellenism_religion')][religion|e]。",
    }
    if key in specials:
        return specials[key]
    return result

def main() -> None:
    translations: dict[str, str] = {}
    for line in SOURCE.read_text(encoding="utf-8-sig").splitlines():
        match = LINE_RE.match(line)
        if match:
            translations[match.group("key")] = translate(match.group("key"), match.group("value"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(translations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(translations)} translations to {OUTPUT}")

if __name__ == "__main__":
    main()
