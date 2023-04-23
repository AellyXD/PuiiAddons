"""
**Get Answers from WriteSonic AI**

✘ Commands Available:
> `{i}sonic` <input>

✘ Example:
> `{i}sonic Who is President of USA right now?`
"""

from . import async_searcher, LOGS, udB, puii_cmd


@puii_cmd(
    pattern="sonic( ([\s\S]*)|$)",
)
async def writesonic(e):
    api_key = udB.get_key("WRITESONIC_API")
    if not api_key:
        return await e.eor(
            "Add `WRITESONIC_API` key in Your Database to use this Plugin. \n\n[Click Here to Get your API key](https://docs.writesonic.com/reference/finding-your-api-key)",
            link_preview=False,
        )
    msg = await e.eor("`Processing...`")
    question = e.pattern_match.group(2)
    if not question and e.is_reply:
        reply = await e.get_reply_message()
        if reply and reply.text:
            question = reply.message
    if not question:
        return await msg.eor("`What should I seek answers for?..`", time=6)

    api_endpoint = (
        "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"
    )
    payload = {
        "enable_google_results": "true",
        "enable_memory": False,
        "input_text": question,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": api_key,
    }
    try:
        response = await async_searcher(
            api_endpoint,
            post=True,
            json=payload,
            headers=headers,
            re_json=True,
        )
        if response and response.get("message"):
            out = "<b>Query:</b>\n{query}\n\n<b>WriteSonic:</b>\n{output}"
            await msg.edit(
                out.format(
                    query=question,
                    output=response.get("message").replace("<br/>", "\n"),
                ),
                parse_mode="html",
            )
        else:
            await msg.edit("`Something Went Wrong`")
            LOGS.info(response)
    except Exception as exc:
        LOGS.warning(exc, exc_info=True)
        await msg.edit(f"**Error:** `{exc}`")
