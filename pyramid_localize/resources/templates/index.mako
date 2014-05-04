<%doc>
 Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>

 This module is part of pyramid_localize and is released under
 the MIT License (MIT): http://opensource.org/licenses/MIT
</%doc>
<%inherit file="pyramid_localize:resources/templates/layout.mako" />
<div class="row">
    <div class="span9">
        <h1>${_('Translations', domain='pyramid_localize')}</h1>
        <p>
            <a href="${request.route_path('localize:update')}" class="btn">${_('Update catalog', domain='pyramid_localize')}</a>
            <a href="${request.route_path('localize:compile')}" class="btn">${_('Compile catalog', domain='pyramid_localize')}</a>
            <a href="${request.route_path('localize:reload')}" class="btn">${_('Reload catalog', domain='pyramid_localize')}</a>
        </p>
        <%include file="_list.mako" />

    </div>
</div>
