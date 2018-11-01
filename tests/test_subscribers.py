"""Subscribers related tests."""
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.i18n import Localizer

# for this tests, these will be imported internally by pyramid's config
# from pyramid_localize.subscribers.i18n import global_renderer
# from pyramid_localize.subscribers.i18n import add_localizer
# from pyramid_localize.subscribers.fake import global_renderer
# from pyramid_localize.subscribers.fake import add_localizer


def test_i18n_new_request(request_i18n):
    """Test if method are being added to request."""
    request_i18n.registry.notify(NewRequest(request_i18n))
    assert isinstance(request_i18n.localizer, Localizer)
    assert hasattr(request_i18n, '_')


def test_i18n_before_render(request_i18n):
    """Test if appropriate methods are being added to render context."""
    before_render_event = BeforeRender({'request': request_i18n}, {})
    request_i18n.registry.notify(before_render_event)
    assert 'localizer' in before_render_event
    assert '_' in before_render_event


def test_i18n_before_render_and_request(request_i18n):
    """Test if appropriate methods are being added to both context and request."""
    request_i18n.registry.notify(NewRequest(request_i18n))
    before_render_event = BeforeRender({'request': request_i18n}, {})
    request_i18n.registry.notify(before_render_event)
    assert 'localizer' in before_render_event
    assert '_' in before_render_event


def test_fake_new_request(request_fake):
    """Test if method are being added to request."""
    request_fake.registry.notify(NewRequest(request_fake))
    assert hasattr(request_fake, '_')


def test_fake_before_render(request_fake):
    """Test if appropriate methods are being added to both context and request."""
    request_fake.registry.notify(NewRequest(request_fake))
    before_render_event = BeforeRender({'request': request_fake}, {})
    request_fake.registry.notify(before_render_event)
    assert '_' in before_render_event


def test_fake_before_render_norequest(request_fake):
    """Test if appropriate methods are being added to render context."""
    before_render_event = BeforeRender({'request': request_fake}, {})
    request_fake.registry.notify(before_render_event)
    assert '_' in before_render_event
