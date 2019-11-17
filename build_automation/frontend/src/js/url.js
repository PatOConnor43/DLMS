const base = process.env.BASE_URL;
const base_url = process.env.NODE_ENV === 'development' ? base || 'http://localhost:8000/' : '';
const APP_URLS = {
    CONTENTS_LIST: base_url + 'api/contents/',
    CONTENT_DETAIL: base_url + 'api/contents/${id}/',
    DIRLAYOUT_LIST: base_url + 'api/dirlayouts/',
    DIRLAYOUT_DETAIL: base_url + 'api/dirlayouts/${id}/',
    DIRLAYOUT_CLONE: base_url + 'api/dirlayouts/${id}/clone/',
    DIRECTORY_LIST: base_url + 'api/directories/',
    DIRECTORY_DETAIL: base_url + 'api/directories/${id}/',
    ALLTAGS_LIST: base_url + 'api/alltags/',
    CREATORS_LIST: base_url + 'api/creators/',
    CREATORS_DETAIL: base_url + 'api/creators/${id}/',
    COVERAGES_LIST: base_url + 'api/coverages/',
    COVERAGES_DETAIL: base_url + 'api/coverages/${id}/',
    SUBJECTS_LIST: base_url + 'api/subjects/',
    SUBJECTS_DETAIL:base_url + 'api/subjects/${id}/',
    KEYWORDS_LIST: base_url + 'api/keywords/',
    KEYWORDS_DETAIL: base_url + 'api/keywords/${id}/',
    WORKAREAS_LIST:base_url + 'api/workareas/',
    WORKAREAS_DETAIL: base_url + 'api/workareas/${id}/',
    LANGUAGES_LIST:base_url + 'api/languages/',
    LANGUAGES_DETAIL:base_url + 'api/languages/${id}/',
    CATALOGERS_LIST:base_url + 'api/catalogers/',
    CATALOGERS_DETAIL:base_url + 'api/catalogers/${id}/',
    START_BUILD: base_url + 'api/dirlayouts/${id}/build/',
    VIEW_BUILD: base_url + 'api/builds/',
    DISKSPACE: base_url + 'api/diskspace/',
    METADATA_UPLOAD: base_url + 'api/metadata/',
    METADATA_MATCH: base_url + 'api/metadata_match',
};
/*
* This function returns a URL
*/
function get_url(templateStringLiteral, context) {
    context = context || {};
    Object.keys(context).forEach(eachKey => {
        templateStringLiteral = templateStringLiteral.replace("${" + eachKey +"}", context[eachKey]);
    });
    return templateStringLiteral;
}

export {
    APP_URLS,
    get_url
};
