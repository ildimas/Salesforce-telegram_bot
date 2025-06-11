import asyncio
from bot.services.async_dict import AsyncDict


def test_set_and_get():
    d = AsyncDict()

    async def run():
        await d.set('foo', 'bar')
        return await d.get('foo')

    result = asyncio.run(run())
    assert result == 'bar'


def test_get_missing_key():
    d = AsyncDict()

    async def run():
        return await d.get('missing')

    result = asyncio.run(run())
    assert result is None


def test_delete():
    d = AsyncDict()

    async def run():
        await d.set('key', 'value')
        await d.delete('key')
        return await d.get('key')

    result = asyncio.run(run())
    assert result is None


def test_keys():
    d = AsyncDict()

    async def run():
        await d.set('a', 1)
        await d.set('b', 2)
        return await d.keys()

    keys = asyncio.run(run())
    assert set(keys) == {'a', 'b'}
