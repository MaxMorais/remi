from remi import gui

from enum import StrEnum

# Container elements

class BaseContainer(gui.Widget):
    def __init__(self, tag = 'div', _class='container', children=None, *args, **kwargs):
        if isinstance(_class, str) and kwargs.pop('fluid', None):
            _class += '-fluid'
        
        super(BaseContainer, self).__init__(self,
            _type=tag,
            _class=_class, 
            *args, 
            **kwargs)

        if children:
            self.append(children)

    def append(self, value, key=''):
        if isinstance(value, (list, tuple, dict)):
            if type(value) == dict:
                for k, v in value.items():
                    self.append(v, k)
                return value.keys()
        
            keys = []
            for child in value:
                keys.append(self.append(child))
            
            return keys
        
        if not isinstance(value, gui.Widget):
            raise ValueError('value should be a Widget (otherwise use add_child(key, other))')
        
        if isinstance(value, str):
            _key = 'text'
        else:
            _key = key or value.identifier
        self.add_child(_key, value)

        return _key


class Header(BaseContainer):
    def __init__(self, fluid=False, children=None, *args, **kwargs):
        super(Header, self).__init__(
            tag='header', 
            fluid=fluid, 
            children=children,
            *args,
            **kwargs)


class Main(BaseContainer):
    def __init__(self, fluid=False, children=None, *args, **kwargs):
        super(Main, self).__init__(
            tag='main', 
            fluid=fluid, 
            children=children,
            *args,
            **kwargs)


class Footer(BaseContainer):
    def __init__(self, fluid=False, children=None, *args, **kwargs):
        super(Footer, self).__init__(
            tag='footer', 
            fluid=fluid, 
            children=children,
            *args,
            **kwargs)


class Body(BaseContainer):
    def __init__(self, fluid=False, children=None, *args, **kwargs):
        super(Body, self).__init__(
            tag='body', 
            fluid=fluid, 
            children=children,
            *args,
            **kwargs)


class Section(BaseContainer):
    def __init__(self, children = None, *args, **kwargs):
        super(Section, self).__init__(
            tag='header', 
            _class=None,  
            children=children,
            *args,
            **kwargs)
        

class RowAlignment(StrEnum):
    START = 'align-start'
    CENTER = 'align-center'
    END = 'align-end'


class Row(BaseContainer):
    def __init__(self, 
            fluid=False, 
            children = None, 
            alignment : RowAlignment = None,
            *args, **kwargs):

        super(Row, self).__init___(
            _class='row',
            fluid=fluid,
            children=children,
            *args,
            **kwargs
        )

        if alignment:
            self.add_class(alignment)


class Col(BaseContainer):
    def __init__(self, col, offset=None, sm=None, md=None, lg=None, xl=None, children=None, *args, **kwargs):
        super(Col, self).__init__(tag='div', _class=f'col-{col}', children=children, *args, **kwargs)

        if offset:
            self.add_class(f'offset-{offset}')

        if sm:
            self.add_class(f'col-sm-{sm}')

        if md:
            self.add_class(f'col-md-{md}')

        if lg:
            self.add_class(f'col-lg-{lg}')
        
        if xl:
            self.add_class(f'col-xl-{xl}')


class Grid(BaseContainer):
    def __init__(self, children = None, *args, **kwargs):
        super(Grid, self).__init__(_class='grid', children=children, *args, **kwargs)


class GridBox(BaseContainer):
    def __init__(self, children = None, *args, **kwargs):
        super(GridBox, self).__init__(_class=None, children=children, *args, **kwargs)


class OverflowAuto(BaseContainer):
    def __init__(self, children = None, *args, **kwargs):
        super(OverflowAuto, self).__init__(_class='overflow-auto', children=children, *args, **kwargs)


class HeadingGroup(BaseContainer):
    def __init__(self, children = None, *args, **kwargs):
        super(HeadingGroup, self).__init__(
            self,
            tag='hgroup',
            _class=None,
            *args,
            **kwargs
        )

# Typografy elements

class BaseTextContainer(BaseContainer):
    def __init__(self, content, *args, **kwargs):
        super(BaseTextContainer, self).__init__(
            tag=self.___class_.__name__.lower(), 
            children=content, 
            *args, 
            **kwargs
        )


class H1(BaseTextContainer):
    """H1 Element"""


class H2(BaseTextContainer):
    """H2 Element"""


class H3(BaseTextContainer):
    """H3 Element"""


class H4(BaseTextContainer):
    """H4 Element"""


class H5(BaseTextContainer):
    """H5 Element"""


class H6(BaseTextContainer):
    """H6 Element"""


class Small(BaseTextContainer):
    """Small Element"""


# Inline Elements

class Abbr(BaseTextContainer):
    """Abbr Element"""


class Strong(BaseTextContainer):
    """Strong Element"""


class B(BaseTextContainer):
    """B Element"""


class I(BaseTextContainer):
    """I Element"""


class Em(BaseTextContainer):
    """EM Element"""


class Cite(BaseTextContainer):
    """Cite Element"""


class Del(BaseTextContainer):
    """Highlighted Element"""


class Ins(BaseTextContainer):
    """Inserted Element"""


class Kbd(BaseTextContainer):
    """Kbd Element"""


class Mark(BaseTextContainer):
    """Highlighted Element"""


class S(BaseTextContainer):
    """Strikethrought element"""


class Sub(BaseTextContainer):
    """Sub element"""


class Sup(BaseTextContainer):
    """Sup element"""


class U(BaseTextContainer):
    """Underline element"""


class Blockquote(BaseTextContainer):
    """Blockquote element"""


class Hr(gui.Widget):
    def __init__(self, *args, **kwargs):
        super(Hr, self).__init__(tag='hr', *args, **kwargs)


# Link Elements

class Variation(StrEnum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    CONTRAST = 'contrast'


class A(BaseTextContainer):
    def __init__(self, href, content, variation : Variation = Variation.PRIMARY, *args, **kwargs):
        super(A, self).__init__(content=content, *args, **kwargs)
        self.attributes['href'] = href

        if variation and variation != Variation.PRIMARY:
            self.add_class(variation)


# Button Elements


class BusyMixin:
    def set_busy(self, is_busy, busy_text = None):
        self._text_backup = self.children.get('text', None)
        if is_busy is True:
            self.attributes['aria-busy'] = 'true'
            if busy_text and self._text_backup:
                self.append(busy_text, 'text')
        elif 'aria-busy' in self.attributes:
            del self.attributes['aria-busy']
            if self._text_backup:
                self.append(self._text_backup, 'text')

class Button(gui.Button, BusyMixin):
    def __init__(self, text, variant: Variation = Variation.PRIMARY, outline : bool = False, *args, **kwargs):
        super(Button, self).__init__(text, *args, **kwargs)

        self.set_outline(outline)
        self.set_variant(variant)

        if variant and variant != Variation.PRIMARY:
            self.add_class(variant)

    def set_outline(self, outline : bool):
        if outline is True:
            self.add_class('outline')
        else:
            self.remove_class('outline')

    def set_variant(self, variant : Variation):
        if variant and variant != Variation.PRIMARY:
            self.add_class(variant)
        else:
            for class_ in (self.attributes['class'] or '').split(' '):
                if class_.startswith('variant-'):
                    self.remove_class(variant)


# Input Elements


class InputMixin:
    def __init__(self):
        self.description = None
        self.validator = None
        self.label = None

    def set_described_by(self, el : Small):
        if not isinstance(el, Small):
            raise TypeError('Inputs only can be described by Small elements')
        
        self.attributes['aria-describedby'] = el.identifier
        self.description = el

    def set_label(self, label):
        if isinstance(label, gui.Label):
            self.attributes['aria-labelledby'] = label.identifier
            self.label = label
            self.label.attributes['for'] = self.identifier
        else:
            self.attributes['aria-label'] = label

    def set_validator(self, validator : callable):
        self.validator = validator

    def set_disabled(self, disabled : bool):
        if disabled:
            self.attributes['disabled'] = None
        elif 'disabled' in self.attributes:
            del self.attributes['disabled']

    def set_valid(self, valid : bool):
        if valid is True:
            self.attributes['aria-invalid'] = 'false'
        elif valid is False:
            self.attributes['aria-invalid'] = 'true'
        elif valid is None and 'aria-invalid' in self.attributes:
            del self.attributes['aria-invalid']


class BaseInput(gui.Input, InputMixin):
    def __init__(self, _type, name, value, *args, **kwargs):
        super(BaseInput, self).__init__(_type, default_value=value, *args, **kwargs)
        self.attributes['name'] = name
        

class Datetime(BaseInput):
    def __init__(self, name, value, *args, **kwargs):
        super(Datetime, self).__init__('datetime', name, value, *args, **kwargs)


class Search(BaseInput):
    def __init__(self, name, value, *args, **kwargs):
        super(Search, self).__init__('search', name, value, *args, **kwargs)


class Color(BaseInput):
    def __init__(self, name, value, *args, **kwargs):
        super(Color, self).__init__('color', name, value, *args, **kwargs)


class File(BaseInput):
    def __init__(self, name, value, *args, **kwargs):
        super(File, self).__init__('file', name, value, *args, **kwargs)


class TextArea(gui.TextInput, InputMixin):
    def __init__(self, name, value, *args, **kwargs):
        super(TextArea, self).__init__(*args, **kwargs)
        self.attributes['name'] = name
        self.set_value(value)


# Selection Elements


class Select(gui.DropDown, InputMixin):
    def __init__(self, name, selected = None, multiple=False, options : list = None, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)
        if options:
            for item in options:
                self.append(item)
        
        if selected:
            self.select_by_value(selected)

        if multiple:
            self.set_multiple(multiple)

    def set_multiple(self, multiple):
        if multiple:
            self.attributes['multiple'] = None
        elif 'multiple' in self.attributes:
            del self.attributes['multiple']


class LabelledInput(gui.Label, InputMixin):
    def __init__(self, text, input, *args, **kwargs):
        super(LabelledInput, self).__init__(text, *kwargs, **kwargs)
        self.add_child('input', input)
        self.input = input

    def set_described_by(self, el: Small):
        self.input.set_described_by(el)
    
    def set_label(self, label : str):
        self.set_text(label)
        self.input.set_label(self)

    def set_validator(self, validator: callable):
        self.input.set_validator(validator)

    def set_disabled(self, disabled : bool):
        self.input.set_disabled(disabled)

    def set_valid(self, valid : bool):
        self.input.set_valid(valid)

    def set_value(self, value):
        self.input.set_value(value)

    def get_value(self):
        return self.input.get_value()
    
    value = property(get_value, set_value)

    @gui.decorate_set_on_listener('(self, emitter, value)')
    @gui.decorate_event
    def onchange(self, value):
        value = value in ('True', 'true')
        self.set_checked(value)
        return (value,)


class LabelledBoxInput(LabelledInput):

    def set_value(self, value : str):
       self.input.attributes['value'] = value

    def get_value(self):
        self.input.attributes.get('value')

    def set_checked(self, checked : bool):
        self.input.set_value(checked)

    def get_checked(self):
        return self.input.get_value()
    
    checked = property(get_checked, set_checked)


class Checkbox(LabelledBoxInput):
    def __init__(self, label, value, checked, *args, **kwargs):

        checkbox = gui.CheckBox(checked, value)

        super(Checkbox, self).__init__(label, checkbox, *args, **kwargs)


class Radiobox(LabelledBoxInput):
    def __init__(self, label, value, checked, *args, **kwargs):
        
        radiobox = gui.CheckBox(checked, value)
        radiobox.type = 'radio'

        super(Radiobox, self).__init__(label, radiobox, *args, **kwargs)


class Switch(Checkbox):
    def __init__(self, label, value, checked, *args, **kwargs):
        super(Switch, self).__init__(label, value, checked, *args, **kwargs)
        self.attributes['role'] = 'switch'


class Range(LabelledInput):
    def __init__(self, label, value, min_val=0, max_val=100, step=1, *args, **kwargs):

        range = gui.Slider(value)

        super(Range, self).__init__(label, range, *args, **kwargs)
        self.set_min(min_val)
        self.set_max(max_val)
        self.set_step(step)

    def set_min(self, min_val):
        if min_val != None:
            self.input.attributes['min'] = min_val
        elif 'min' in self.input.attributes:
            del self.input.attributes['min']

    def set_max(self, max_val):
        if max_val != None:
            self.input.attributes['max'] = max_val
        elif 'max' in self.input.attributes:
            del self.input.attributes['min']

    def step(self, step):
        if step != None:
            self.input.attributes['step'] = step
        elif 'step' in self.input.attributes:
            del self.input.attributes['step']


# InputSet Elements

class Role(StrEnum):
    GROUP = 'group'
    SEARCH = 'search'


class BaseGroup(BaseContainer):
    def __init__(self, tag, role : Role = Role.GROUP, children=None, *args, **kwargs):
        super(BaseGroup, self).__init__(tag, 'group', children, *args, **kwargs)
        self.attributes['role'] = role


class Fieldset(BaseGroup):
    def __init__(self, legend = None, children = None, role : Role = Role.GROUP, *args, **kwargs):
        super(Fieldset, self).__init__('fieldset', role=role, children=None, *args, **kwargs)

        self.set_legend(legend)
        self.append(children)

    def set_legend(self, text):
        self.legend = gui.Tag(_type='legend')
        self.legend.add_child('text', text)

        self.append(self.legend, 'legend')


class Form(BaseGroup):
    def __init__(self, children = None, role : Role = None, *args, **kwargs):
        pass


# Components

class WithSummaryMixin:
    def set_title(self, title):
        if not self.title:
            self.title = gui.Tag(_type='summary')
            self.append(title, 'title')
        self.title.add_child('text', title)

    def set_as_button(self, as_button):
        if as_button is True:
            self.title.attributes['role'] = 'button'
        elif 'role' in self.attributes:
            del self.title.attributes['role']


class Accordion(BaseContainer, WithSummaryMixin, BusyMixin):
    def __init__(self, title, content, is_open = False, as_button=False, variant : Variation = None, outline = False, *args, **kwargs):
        super(Accordion, self).__init__('details', *args, **kwargs)

        self.set_title(title)
        self.append(content, 'content')

        self.toggle(is_open)
        self.set_as_button(as_button)
        self.set_variant(variant)
        self.set_outline(outline)

    def toggle(self, is_open):
        if is_open is True:
            self.title.attributes['open'] = None
        elif 'open' in self.attributes:
            del self.title.attributes['open']

    def set_outline(self, outline : bool):
        if outline is True:
            self.title.add_class('outline')
        else:
            self.title.remove_class('outline')

    def set_variant(self, variant : Variation):
        if variant and variant != Variation.PRIMARY:
            self.title.add_class(variant)
        else:
            for class_ in (self.title.attributes['class'] or '').split(' '):
                if class_.startswith('variant-'):
                    self.title.remove_class(variant)


class Article(BaseContainer):
    def __init__(self, children = None, role : Role = None, *args, **kwargs):
        super(Article, self).__init__(tag='article', children=children, *args, **kwargs)


class Dropdown(BaseContainer, WithSummaryMixin):
    def __init__(self, title, children, *args, **kwargs):
        super(Dropdown, self).__init__(tag='details', _class='dropdown', *args, **kwargs)
        
        self.set_title(title)
        self.append(children)


class BusyIndicator(gui.Tag, BusyMixin):
    def __init__(self, text):
        super(BusyIndicator, self).__init__(_type='span')
        self.set_busy(True, text)