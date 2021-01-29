<%doc>
 Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>

 This module is part of pyramid_localize and is released under
 the MIT License (MIT): http://opensource.org/licenses/MIT
</%doc>
<table class="table table-hover">
    <thead>
        <tr>
            <th>${_('Language', domain='pyramid_localize')}</th>
            <th>${_('Translation domain', domain='pyramid_localize')}</th>
            <th>${_('${type} modification time', domain='pyramid_localize', mapping={'type': 'pot'})}</th>
            <th>${_('${type} modification time', domain='pyramid_localize', mapping={'type': 'po'})}</th>
            <th>${_('${type} modification time', domain='pyramid_localize', mapping={'type': 'mo'})}</th>
        </tr>
    </thead>
    <tbody>
        % for language in translations:
            <tr>
                <td rowspan="${len(translations[language]) if len(translations[language]) > 1 else 1}">${language}</td>
                % for domain in translations[language]:
                        <td>${domain}</td>
                        <td>${translations[language][domain]['pot']}</td>
                        <td>${translations[language][domain]['po']}</td>
                        <td>${translations[language][domain]['mo']}</td>
                    % if len(translations[language]) > 1:
                        </tr><tr>
                    % endif
                % endfor
            </tr>
        % endfor
    </tbody>
</table>
