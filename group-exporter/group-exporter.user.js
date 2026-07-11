// ==UserScript==
// @name         group-exporter
// @namespace    https://github.com/hugoschool/intranet-utils
// @version      v1.0.0
// @description  UserScript to export all groups from a project
// @author       Hugo ARNAL (@hugoarnal)
// @match        https://intra.epitech.eu/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const SERVER_URL = "http://localhost:8000";

    const GROUPS_REGEX = /registered: (.*),$/m;
    const URL_REGEX = /https:\/\/intra\.epitech\.eu\/module\/[0-9]{4}\/([a-zA-Z]-[a-zA-Z]{3}-[0-9]{3})\/.*\/group$/m;

    let urlRegex = URL_REGEX.exec(window.location.href);
    if (urlRegex !== null) {
        const projectName = document.querySelector("[title=\"Project title\"]").innerText;
        const moduleCode = urlRegex[1];
        const groupsText = document.querySelectorAll("script")[8].innerText;

        let groupsRegex = GROUPS_REGEX.exec(groupsText);
        if (groupsRegex !== null) {
            const groups = JSON.parse(groupsRegex[1]);

            console.log("[group-exporter] Sent request to export all groups")
            fetch(`${SERVER_URL}/group-page`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"module": {"code": moduleCode}, "project": {"name": projectName}, "content": groups})
            }).then((response) => {
                if (response.status !== 200) {
                    response.text().then((text) => console.log(text))
                }
            });
        }
    }
})();
