import os
import posixpath
import pandas as pd
import numpy as np

# use double curly braces {{}} for any 'LaTeX' curly braces
# and single curly braces {} for any python formatting 
swfig = r"""
\begin{{sidewaysfigure}}{0}
    \centering
    \includegraphics[{1}]{{{2}}}{3}{4}
\end{{sidewaysfigure}}"""

#\caption{{{1}}}
#\label{{fig:{2}}}

normalfig = r"""
\begin{{figure}}{0}
    \centering
    \includegraphics[{1}]{{{2}}}{3}{4}
\end{{figure}}"""


def _process_file(f, func, **kwargs):
    return func(f, **kwargs)

    
def with_file(f, func, **kwargs):
    """Applies function func to the file handle f.
    If f is an open file object, it will stay open.
    If f is not open, it will be opened then closed again after
    processing before returning.
    """
    if hasattr(f, 'read'):
        return func(f, **kwargs)
    else:
        mode = kwargs.get('filemode', 'a')
        with open(f, mode) as f:
            return func(f, **kwargs)

            
def create_dirs(dir_list):
    """Creates all directories in the list of directories
    if they do not already exist.
    """
    for d in dir_list:
        if not os.path.exists(d):
            os.makedirs(d)

            
def fixed(x, sig=3):
    """Returns the value x as a text string in fixed format
    with the number of decimals specified by argument sig.
    """
    txt = '{{0:.{0:d}f'.format(sig) + '}'
    if np.isnan(x):
        return ''
    else:
        return txt.format(x)

        
def scientific(x, sig=3, tex=True):
    """Returns the value x as a text string in scientific format
    with the number of decimals specified by argument sig.
    If argument tex is True, the text string will be tex formated.
    It is assumed that the package siunitx is used.
    """
    txt_tex = '\\num{{{0:.'+'{0:d}e'.format(sig) + '}}}'
    txt = '{{0:.{0:d}e'.format(sig) + '}'
    if np.isnan(x):
        return ''
    else:
        if tex:
            return txt_tex.format(x)
        else:
            return txt.format(x)

            
def append_figure(file, figfilepath, sideways=False, caption=None, label=None, 
                  loc='[htp]', width='\linewidth', fig_args=''):
    """Adds figure to tex file.
    
    Parameters
    ----------
    file: open file object
        text file to append figure to
    figfilepath: string
        path and filename of figure file
    sideways: boolean
        flag to turn figure sideways
    caption: string
        tex string to include as caption
    label: string
        the label to add after 'fig:'
    loc: string
        the figure location specifier
    width: string
        width argument to pass to includegraphics
    fig_args: string
        additional arguments to pass to includegraphics
    """
    if sideways:
        txt = swfig
    else:
        txt = normalfig
    
    if caption is not None:
        cap = '\n\caption{{{0}}}'.format(caption)
    else:
        cap = ''
    
    if label is not None:
        lab = '\n\label{{fig:{0}}}'.format(label)
    else:
        lab = ''
    
    args = 'width={0}'.format(width)
    if fig_args:
        args = args+',{0}'.format(fig_args)
    file.write(txt.format(loc, args, figfilepath, cap, lab)+'\n\n')

    
def append_table(file, df, na_rep='', small=True, sideways=False, centering=False, 
                 loc='[htp]', caption=None, caption_above=True, label=None, 
                 threeparttable=False, tablenotes='', **kwargs):
    """Adds table to tex file, table should be passed as a pandas dataframe.
    
    Parameters
    ----------
    file: open file object
        text file to append figure to
    df: DataFrame object
        the table to add
    na_rep: string
        string to use when substituting na values
    small: boolean
        use small text font
    sideways: boolean
        flag to turn figure sideways
    centering: boolean
        flag to center table on page
    loc: string
        the figure location specifier
    caption: string
        tex string to include as caption
    caption_above: bool
        wether caption is typeset above or below table
    label: string
        the label to add after 'tab:'
    threeparttable: boolean
        flag to use threeparttable
    tablenotes: string
        any footnotes to be typeset below the table, this automatically
        sets the threeparttable flag to True
        sets the caption_above flag to True
    kwargs: dictionary
        additional keyword arguments to pass to df.to_latex
    """
    
    if tablenotes is not None or tablenotes != "":
        threeparttable = True
        caption_above = True

    if sideways:
        file.write('\\begin{turn}{90}\n')
        file.write('\\begin{minipage}{0.9\\textheight}\n')
        file.write('\\begin{table}[H]\n')
    else:
        file.write('\\begin{{table}}{0}\n'.format(loc))

    if centering:
        file.write('\\centering\n')
    
    if threeparttable:
        file.write('\\begin{threeparttable}\n')
        
    if small:
        file.write('\\small\n')
    
    if caption is not None:
        cap = '\n\caption{{{0}}}'.format(caption)
    else:
        cap = ''
    
    if label is not None:
        lab = '\n\label{{tab:{0}}}'.format(label)
    else:
        lab = ''

    if caption_above:
        file.write(cap)
        file.write(lab+'\n')
        
    txt = df.to_latex(na_rep=na_rep, **kwargs)
    file.write(txt)

    
    if not caption_above:
        file.write(cap)
        file.write(lab+'\n')
        
    if threeparttable:
        file.write('\\begin{tablenotes}\n')
        file.write(tablenotes)
        file.write('\n')
        file.write('\\end{tablenotes}\n')
        file.write('\end{threeparttable}\n')
    
    file.write('\\end{table}')

    if sideways:
        file.write('\\end{minipage}\n')
        file.write('\\end{turn}\n')
    
    file.write('\n\n')

    
def append_section_heading(file, secname, label=None, indent=0):
    if label is None:
        file.write('{0}\\section{{{1}}}\n\n'.format( ' '*indent,secname))
    else:
        file.write('{0}\\section{{{1}}}\label{{{2}}}\n\n'.format( ' '*indent,secname,label))
    

def append_newpage(file):
    file.write('\\clearpage\n\n')

    
def append_chapter_title(file, title, label=None):
    txt = '\chapter{{{0}}}'.format(title)
    if label is not None:
        txt += '\label{{{0}}}'.format(label)
    
    file.write(txt+'\n\n')
    
"""
EXAMPLE OF HOW PACKAGE COULD BE USED:
    
def produce_latex_file(info):
    config = info['config']
    sample_info = info['sample']
    history = info['history']
    interpret = info['interpret']
    latex_info = info['latex']

    if not latex_info['produce_latex_file']:
        return
        
    steps = sorted([d['step'] for d in history])
    
    with open(latex_info['filename'], 'w') as f:
        
        append_chapter_title(f, 'Sample "{0}"'.format(sample_info['name']), 
                             label='app:{0}'.format(sample_info['nickname'].lower().replace(' ','_')))

        append_section_heading(f,'Consolidation curve')
        
        tcname = posixpath.join('.', latex_info['figspath'], 'consolidation_curve.png')
        append_normal_figure(f, tcname, loc='[hp!]')
        
        sifo = [['Name', sample_info['name']],
                ['Depth', sample_info['depth']],
                #['Initial height', '{0} mm'.format(sample_info['h0'])],
                #['Diameter', '{0:.1f} mm'.format(sample_info['diameter'])],
                ['Start date', history[0]['date']],
                ['End date', history[-1]['date2']]
                ]
        
        df = pd.DataFrame(sifo, columns=['Parameter','Value'])
        append_table(f, df, centering=True, index=False)
        
        append_newpage(f)
        
        cfname, cfext = os.path.splitext(os.path.basename(latex_info['filename']))
        cfname = cfname + '_classification.tex'
        
        f.write('\\IfFileExists{{./{0}}}{{\n'.format(cfname))
        append_section_heading(f, 'Classification parameters', indent=4)
        f.write('    \\input{{./{0}}}\n'.format(cfname))
        f.write('    \\clearpage\n')
        f.write('}{}\n\n')
        
        append_section_heading(f, 'Overview of load steps and interpreted results')
        
        if os.path.exists(latex_info['interpretation_file']):
            results = pd.read_excel(latex_info['interpretation_file'], sheetname='results')
            

                        
            formatters = {'step':   lambda x: fixed(x, 0),
                          'load':   lambda x: fixed(x, 1),
                          'temp':   lambda x: fixed(x, 1),
                          'eps0':   lambda x: fixed(x, 3),
                          'eps50':  lambda x: fixed(x, 3),
                          'eps90':  lambda x: fixed(x, 3),
                          'eps100': lambda x: fixed(x, 3),
                          'epsf':   lambda x: fixed(x, 3),
                          't50':    lambda x: fixed(x, 3),
                          't90':    lambda x: fixed(x, 3),
                          't100':   lambda x: fixed(x, 3),
                          'epss':   lambda x: fixed(x, 3),
                          'Cv':     lambda x: scientific(x, 3),
                          'K':      lambda x: fixed(x, 0),
                          'k0':     lambda x: scientific(x, 3)
                         }
            

            columns = ['step',
                       'load',
                       'temp', 
                       'eps0',
                       'eps50', 
                       'eps100',
                       'epsf',
                       'epss', 
                       'Cv',   
                       'K',    
                       'k0']
            
            dropcols = [col for col in results.columns if col not in columns]
            df = results.drop(labels=dropcols, axis=1, inplace=False)                
            cols = [col for col in columns if col in df.columns]
            
            # Since we are using siunitx to typeset the columns, 
            # non-numerical cell contents must be braced...
            headers = ['{Step}', 
                       '{$\\sigma$ [\si{kPa}]}', 
                       '{$T$ [\si{\celsius}]}',
                       '{$\\varepsilon_{0}$ [\%]}',
                       '{$\\varepsilon_{50}$ [\%]}',
                       '{$\\varepsilon_{100}$ [\%]}',
                       '{$\\varepsilon_{f}$ [\%]}',
                       '{$C_{\\alpha}$ [\%/lct]}',
                       '{$c_v$ [\si{m^2/s}]}',
                       '{$K$ [\si{kPa}]}',
                       '{$k_0$ [\si{m/s}]}']                       

                       
            heads = [headers[id] for id, col in enumerate(columns) if col in df.columns]
                        
            append_table(f, df, centering=True, sideways=True, loc='[H]', columns=cols, header=heads, 
                        na_rep='', index=False, escape=False, formatters=formatters,
                        column_format='c'*len(heads))
                        
        else:
            f.write('Interpretation data is missing...\n')
        
        append_newpage(f)

        fname = posixpath.join('.', latex_info['figspath'], 'lvdt_strain_full.png')
        append_sideways_figure(f, fname)

        append_newpage(f)        
        
        f.write('\\iftimecurves\n')
        f.write('\\fakesection{Time curves}\n\n')
        
        for hist in info['history']:
            ovname = '{0:02.0f}_{1}_raw_{2:g}kPa_{3:g}C.png'.format(hist['step'], 
                                                                    info['sample']['name'].replace(' ','-'),
                                                                    hist['load'], hist['temp'])
            ovname = posixpath.join('.', latex_info['figspath'], ovname)
            append_sideways_figure(f, ovname)

            tcname = '{0:02.0f}_{1}_timec_{2:g}kPa_{3:g}C.png'.format(hist['step'], 
                                                                      info['sample']['name'].replace(' ','-'),
                                                                      hist['load'], hist['temp'])
            tcname = posixpath.join('.', latex_info['figspath'], tcname)
            append_normal_figure(f, tcname)
            
            append_newpage(f)
    
        f.write('\\fi\n')
"""
