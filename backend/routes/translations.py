from fastapi import APIRouter, HTTPException, status, Depends
from models.users import User
from models.translations import (
    Language,
    LanguageUpdate,
    TranslationPage,
    TranslationEntry,
    Translation
)
from database import db_languages, db_translations
from schemas import (
    LanguageSerializer,
    TranslationPageSerializer
)
from deps import get_current_user
import pymongo

router = APIRouter(prefix='/translations')

tag_lang = 'Working with languages'
tag_translate = 'Working with translations'


@router.get(
    "/languages",
    status_code=status.HTTP_200_OK,
    summary='Returns the list of all languages.',
    tags=[tag_lang]
)
async def get_languages():

    language = LanguageSerializer.list_serialize(
        db_languages.find().sort(
            [
                ("code", pymongo.ASCENDING),
                ("language", pymongo.ASCENDING)
            ]
        )
    )

    return language


@router.get(
    "/languages/{code}",
    status_code=status.HTTP_200_OK,
    summary='Gets language by its code.',
    tags=[tag_lang]
)
async def get_language(code: str):

    language = LanguageSerializer.serialize(
        db_languages.find_one({"code": code})
    )

    if language is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language doesn't exist."
        )

    return language


@router.post(
    "/languages/new",
    status_code=status.HTTP_200_OK,
    summary='Creates new language entry.',
    tags=[tag_lang]
)
async def add_language(lang: Language, user: User = Depends(get_current_user)):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    language = LanguageSerializer.serialize(
        db_languages.find_one({"code": lang.code})
    )

    if language is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language already exists."
        )

    db_languages.insert_one(dict(Language(code=lang.code, name=lang.name)))

    return {"message": "Language was added!"}


@router.put(
    "/languages/{code}/update",
    status_code=status.HTTP_200_OK,
    summary='Updates language from the list.',
    tags=[tag_lang]
)
async def update_language(
    code: str,
    update: LanguageUpdate,
    user: User = Depends(get_current_user)
):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    language = LanguageSerializer.serialize(
        db_languages.find_one({"code": code})
    )

    if language is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language doesn't exist."
        )

    db_languages.update_one({"code": code}, {"$set": {"name": update.name}})

    return {"message": "Language was updated!"}


@router.delete(
    "/languages/{code}/delete",
    status_code=status.HTTP_200_OK,
    summary='Deletes a language from the list.',
    tags=[tag_lang]
)
async def remove_language(code: str, user: User = Depends(get_current_user)):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    language = LanguageSerializer.serialize(
        db_languages.find_one({"code": code})
    )

    if language is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language doesn't exist."
        )

    db_languages.delete_one({"code": code})

    return {"message": "Language was removed!"}


@router.get(
    "/pages",
    status_code=status.HTTP_200_OK,
    summary='Returns the list of all translation pages.',
    tags=[tag_translate]
)
async def get_pages():

    pages = TranslationPageSerializer.list_serialize(
        db_translations.find().sort(
            [
                ("page_name", pymongo.ASCENDING)
            ]
        )
    )

    return pages


@router.get(
    "/pages/{page_name}",
    status_code=status.HTTP_200_OK,
    summary='Returns a translation page by its name.',
    tags=[tag_translate]
)
async def get_page(page_name: str):

    page = TranslationPageSerializer.serialize(
        db_translations.find_one({"name": page_name})
    )

    return page


@router.post(
    "/pages/new",
    status_code=status.HTTP_200_OK,
    summary='Creates new translation page.',
    tags=[tag_translate]
)
async def add_page(
    page: TranslationPage,
    user: User = Depends(get_current_user)
):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    same_page = TranslationPageSerializer.serialize(
        db_translations.find_one({"name": page.name})
    )

    if same_page is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation page already exists."
        )

    db_translations.insert_one(
        dict(TranslationPage(name=page.name, entries=[]))
    )

    return {"message": "Translation page was added!"}


@router.delete(
    "/pages/{page_name}/delete",
    status_code=status.HTTP_200_OK,
    summary='Deletes a translation page.',
    tags=[tag_translate]
)
async def delete_page(page_name: str, user: User = Depends(get_current_user)):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    page = TranslationPageSerializer.serialize(
        db_translations.find_one({"name": page_name})
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation page doesn't exists."
        )

    db_translations.delete_one({"name": page_name})

    return {"message": "Translation page was deleted!"}


@router.post(
    "/pages/{page_name}/new_entry",
    status_code=status.HTTP_200_OK,
    summary='Creates new translation entry at the selected translation page.',
    tags=[tag_translate]
)
async def add_translation_entry(
    page_name: str,
    entry: TranslationEntry,
    user: User = Depends(get_current_user)
):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    page = TranslationPageSerializer.serialize(
        db_translations.find_one({"name": page_name})
    )

    entries_keys = [e['key'] for e in page['entries']] if page else []

    if entry.key in entries_keys:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation entry already exists."
        )

    db_translations.update_one(
        {"name": page_name},
        {
            "$addToSet": {
                'entries': {
                    "key": entry.key,
                    "translations": {}
                }
            }
        }
    )

    return {"message": "Translation entry was added!"}


@router.delete(
    "/pages/{page_name}/{entry_key}/delete",
    status_code=status.HTTP_200_OK,
    summary='Deletes a translation entry at the selected translation page.',
    tags=[tag_translate]
)
async def del_translation_entry(
    page_name: str,
    entry_key: str,
    user: User = Depends(get_current_user)
):

    if "admin" not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin rights are required."
        )

    page = TranslationPageSerializer.serialize(
        db_translations.find_one({"name": page_name})
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation page doesn't exist."
        )

    entries_keys = [e['key'] for e in page['entries']] if page else []

    if entry_key not in entries_keys:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation entry doesn't exist."
        )

    db_translations.update_one(
        {"name": page_name},
        {"$pull": {'entries': {"key": entry_key}}}
    )

    return {"message": "Translation entry was deleted!"}


@router.get(
    "/pages/{page_name}/{entry_key}/{lang}",
    status_code=status.HTTP_200_OK,
    summary='Get a translation for an entry at the selected translation page.',
    tags=[tag_translate]
)
async def get_translation_entry_lang(
    page_name: str,
    entry_key: str,
    lang: str
):

    page = TranslationPageSerializer.serialize(
        db_translations.find_one({"name": page_name})
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation page doesn't exist."
        )

    entries_keys = [e['key'] for e in page['entries']] if page else []

    if entry_key not in entries_keys:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation entry doesn't exist."
        )
        
    entry = {'translations': {}}
    
    for cur_entry in page['entries']:
        if cur_entry['key'] == entry_key:
            entry = cur_entry
            break
    
        
    return { "translation": entry['translations'].get(lang, 'undefined')}


@router.put(
    "/pages/{page_name}/{entry_key}/{lang}/set",
    status_code=status.HTTP_200_OK,
    summary='Set a translation for an entry at the selected translation page.',
    tags=[tag_translate]
)
async def set_translation_entry_lang(
    page_name: str,
    entry_key: str,
    lang: str,
    translation: Translation,
    user: User = Depends(get_current_user)
):

    print(user.roles, lang)
    if (lang not in user.roles) and ("admin" not in user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have no rights for this language."
        )

    page = TranslationPageSerializer.serialize(
        db_translations.find_one({"name": page_name})
    )

    if page is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation page doesn't exist."
        )

    entries_keys = [e['key'] for e in page['entries']] if page else []

    if entry_key not in entries_keys:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Translation entry doesn't exist."
        )

    db_translations.update_one(
        {
            "name": page_name,
            "entries.key": entry_key
        },
        {
            "$set": {
                f'entries.$.translations.{lang}': translation.text
            }
        }
    )

    return {"message": "Translation entry lang was set!"}
