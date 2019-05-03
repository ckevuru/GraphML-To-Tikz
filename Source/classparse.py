'''
This class is the complete backbone of the entire module and handles backend completely. The conversion from  GraphML to Tikz actually happens in this file.
'''

import os
import sys
import argparse
import xml.dom.minidom

from xml.dom.minidom import parse
from collections import OrderedDict


class ParseTikz:
    '''Dictionary for finding shape equivalents.
    '''
    shape_dict = {'ellipse': 'circle', 'diamond': 'diamond', 'trapezoid': 'trapezium',
                  'trapezoid2': 'trapezium, rotate=180',
                  'hexagon': 'regular polygon, regular polygon sides=6',
                  'octagon': 'regular polygon, regular polygon sides=6',
                  'star5': 'star, star points=5', 'star6': 'star, star points=6',
                  'star7': 'star, star points=7', 'star8': 'star, star points=8',
                  'triangle': 'regular polygon, regular polygon sides = 3',
                  'triangle2': 'regular polygon, regular polygon sides = 3, rotate=180',
                  'circle': 'circle', 'rectangle': 'rectangle', 'rectangle3d': 'rectangle',
                  'roundrectangle': 'rectangle, rounded corners = 1', 'parallelogram': 'trapezium',
                  'parallelogram2': 'trapezium','fatarrow': 'circle', 'fatarrow2': 'circle'}

    '''Dictionary for determining directed vs undirected.
    '''
    arrow_dict = {'standard': True, 'none': False}

    label_dict = {}

    bez_control = {}

    def __init__(self):
        self.file_output = 'temp_out.tex'

    def dummyargs(self):
        max_xe = [], min_xe = [], max_ye = [], min_ye = [], node_list = [], edge_list = []
        return max_xe, min_xe, max_ye, min_ye, node_list, edge_list

    def normalize(self, x, y, max_x, max_y, min_x, min_y):
        '''Function for handling scale conversions.
        '''
        scale = float(max(max_x-min_x,max_y-min_y))
        if scale == 0:
            return 0, 0
        else:
            return round(float(x)/float(scale),2), round(float(y)/float(scale),2)
    
    def getTikzFile(self, file_input, flag):
        '''Function for determinig success or failure of conversion.
        '''
        self.file_input = file_input
        self.flag = flag
        max_xe, min_xe, max_ye, min_ye, node_list, edge_list, exflag, exception = self.parse_xml()
        if exflag == True:
            return exflag, exception, ''
        else:
            contents = self.drawTikzgraph(max_xe, min_xe, max_ye, min_ye, node_list, edge_list)
            os.remove(self.file_output)
            return exflag, exception, contents

    def getNonEmptyLabel(self, nodelabel):
        '''Function for finding non empty text label if it exists.
        '''
        for label in nodelabel:
            if (label.childNodes[0].nodeValue).strip() != '':
                return label
        return ''

    def parse_xml(self):
        '''Function for complete extraction of information from .graphml files and error handling.
        '''
        try:
            DOMTree = xml.dom.minidom.parse(self.file_input)
            collection = DOMTree.documentElement
        except Exception as e:
            return [], [], [], [], [], [], True, 'Prase Error : ' + str(e)

        graphs = collection.getElementsByTagName('graph')

        if len(graphs) == 0:
            return [], [], [], [], [], [], True, 'Conversion Error : No graph elements found in file'

        node_list = []
        edge_list = []

        for graph in graphs:
            nodes = graph.getElementsByTagName('node')
            if nodes != '':
                try:
                    for node in nodes:
                        dict = {}
                        geo = node.getElementsByTagName('y:Geometry')[0]
                        fill = node.getElementsByTagName('y:Fill')[0]
                        border = node.getElementsByTagName('y:BorderStyle')[0]
                        nodelabel = node.getElementsByTagName('y:NodeLabel')
                        shape = node.getElementsByTagName('y:Shape')[0]
                        nonemptylabel = self.getNonEmptyLabel(nodelabel)
                        dict['id'] = node.getAttribute('id')
                        if nonemptylabel == '':
                            dict['label'] = ''
                            dict['text_color'] = '#000000'
                        else:
                            dict['label'] = nonemptylabel.childNodes[0].nodeValue
                            dict['text_color'] = nonemptylabel.getAttribute(
                                'textColor')
                            dict['labelfontsize'] = nonemptylabel.getAttribute(
                                'fontSize')
                            dict['labelfontstyle'] = nonemptylabel.getAttribute(
                                'fontStyle')

                        dict['x'] = float(geo.getAttribute('x'))
                        dict['y'] = float(geo.getAttribute('y'))
                        dict['height'] = geo.getAttribute('height')
                        dict['width'] = geo.getAttribute('width')
                        dict['fill'] = fill.getAttribute('color')
                        dict['bordercolor'] = border.getAttribute('color')
                        dict['thick'] = border.getAttribute('width')
                        self.label_dict[dict['id']] = dict['label']
                        dict['shape'] = shape.getAttribute('type')
                        node_list.append(dict)

                except Exception as ex:
                    return [], [], [], [], [], [], True, 'Node/Attribute Error for node element : ' + str(ex)

            edges = graph.getElementsByTagName('edge')
            if edges != '':
                max_xe = []
                min_xe = []
                max_ye = []
                min_ye = []
                try:
                    for edge in edges:
                        dict = {}
                        cont_list = []
                        dict['id'] = edge.getAttribute('id')
                        dict['source'] = edge.getAttribute('source')
                        dict['target'] = edge.getAttribute('target')
                        line = edge.getElementsByTagName('y:LineStyle')[0]
                        edgeLabel = edge.getElementsByTagName('y:EdgeLabel')
                        arrow = edge.getElementsByTagName('y:Arrows')[0]
                        polyedge = edge.getElementsByTagName('y:PolyLineEdge')
                        arcedge = edge.getElementsByTagName('y:ArcEdge')
                        bezedge = edge.getElementsByTagName('y:BezierEdge')
                        qadedge = edge.getElementsByTagName('y:QuadCurveEdge')
                        spledge = edge.getElementsByTagName('y:SplineEdge')
                        shallow = edge.getElementsByTagName('y:GenericEdge')
                        nonemptylabel = self.getNonEmptyLabel(edgeLabel)
                        if nonemptylabel == '':
                            dict['label'] = ''
                            dict['text_color'] = '#000000'
                        else:
                            dict['label'] = nonemptylabel.childNodes[0].nodeValue
                            dict['text_color'] = nonemptylabel.getAttribute(
                                'textColor')
                            dict['labelfontsize'] = nonemptylabel.getAttribute(
                                'fontSize')
                            dict['labelfontstyle'] = nonemptylabel.getAttribute(
                                'fontStyle')
                        if len(polyedge) != 0 or len(shallow) != 0:
                            if len(shallow) != 0:
                                polyedge = shallow
                            dict['polyedge'] = True
                            dict['arcedge'] = False
                            dict['bezedge'] = False
                            dict['spledge'] = False
                            dict['pclist'] = False
                            cpoints = polyedge[0].getElementsByTagName('y:Point')
                            if len(cpoints) != 0:
                                for cp in cpoints:
                                    ct = [cp.getAttribute(
                                        'x'), cp.getAttribute('y')]
                                    max_xe.append(float(ct[0]))
                                    min_xe.append(float(ct[0]))
                                    max_ye.append(float(ct[1]))
                                    min_ye.append(float(ct[1]))
                                    cont_list.append(ct)
                                dict['pclist'] = True

                            dict['clist'] = cont_list

                        elif len(arcedge) != 0:
                            dict['arcedge'] = True
                            dict['polyedge'] = False
                            dict['bezedge'] = False
                            dict['spledge'] = False
                            cpoints = arcedge[0].getElementsByTagName('y:Point')
                            for cp in cpoints:
                                ct = [cp.getAttribute('x'), cp.getAttribute('y')]
                                cont_list.append(ct)
                                max_xe.append(float(ct[0]))
                                min_xe.append(float(ct[0]))
                                max_ye.append(float(ct[1]))
                                min_ye.append(float(ct[1]))

                            dict['clist'] = cont_list

                        elif len(spledge) != 0:
                            dict['spledge'] = True
                            dict['arcedge'] = False
                            dict['polyedge'] = False
                            dict['bezedge'] = False
                            cpoints = spledge[0].getElementsByTagName('y:Point')
                            for cp in cpoints:
                                ct = [cp.getAttribute('x'), cp.getAttribute('y')]
                                cont_list.append(ct)
                                max_xe.append(float(ct[0]))
                                min_xe.append(float(ct[0]))
                                max_ye.append(float(ct[1]))
                                min_ye.append(float(ct[1]))

                            dict['clist'] = cont_list

                        elif len(bezedge) != 0 or len(qadedge) != 0:
                            if len(qadedge) != 0:
                                bezedge = qadedge
                            dict['bezedge'] = True
                            dict['polyedge'] = False
                            dict['arcedge'] = False
                            dict['spledge'] = False
                            cont_list = []
                            cpoints = bezedge[0].getElementsByTagName('y:Point')
                            for cp in cpoints:
                                ct = [cp.getAttribute('x'), cp.getAttribute('y')]
                                max_xe.append(float(ct[0]))
                                min_xe.append(float(ct[0]))
                                max_ye.append(float(ct[1]))
                                min_ye.append(float(ct[1]))
                                cont_list.append(ct)

                            dict['clist'] = cont_list

                        else:
                            dict['bezedge'] = False
                            dict['polyedge'] = False
                            dict['arcedge'] = False
                            dict['spledge'] = False

                        dict['directed'] = arrow.getAttribute('target')
                        dict['linecolor'] = line.getAttribute('color')
                        dict['linetype'] = line.getAttribute('type')
                        dict['arrow_src'] = arrow.getAttribute('source')
                        dict['arrow_tar'] = arrow.getAttribute('target')
                        dict['thick'] = line.getAttribute('width')
                        edge_list.append(dict)
                
                except Exception as ex:
                    return [], [], [], [], [], [], True, 'Edge/Attribute Error for edge element : ' + str(ex)

        return max_xe, min_xe, max_ye, min_ye, node_list, edge_list, False, ''

    def getAllColors(self, node):
        '''Function for parsing colors in .graphml to tikz format for nodes.
        '''
        node_fill_color = '\\definecolor{%s}{RGB}' % (node['id']+'fill')
        node_hex = node['fill'].lstrip('#')
        node_color = tuple(int(node_hex[i:i+2], 16) for i in (0, 2, 4))
        ncolor = node_fill_color + \
            '{%s,%s,%s}' % (str(node_color[0]), str(
                node_color[1]), str(node_color[2])) + '\n'

        text_fill_color = '\\definecolor{%s}{RGB}' % (node['id']+'text')
        text_hex = node['text_color'].lstrip('#')
        text_color = tuple(int(text_hex[i:i+2], 16) for i in (0, 2, 4))
        tcolor = text_fill_color + \
            '{%s,%s,%s}' % (str(text_color[0]), str(
                text_color[1]), str(text_color[2])) + '\n'

        border_fill_color = '\\definecolor{%s}{RGB}' % (node['id']+'draw')
        border_hex = node['bordercolor'].lstrip('#')
        border_color = tuple(int(border_hex[i:i+2], 16) for i in (0, 2, 4))
        bcolor = border_fill_color + \
            '{%s,%s,%s}' % (str(border_color[0]), str(
                border_color[1]), str(border_color[2])) + '\n'

        return ncolor, tcolor, bcolor

    def getEdgeColors(self, node):
        '''Function for parsing colors in .graphml to tikz format for edges.
        '''
        node_fill_color = '\\definecolor{%s}{RGB}' % (node['id']+'draw')
        node_hex = node['linecolor'].lstrip('#')
        node_color = tuple(int(node_hex[i:i+2], 16) for i in (0, 2, 4))
        ncolor = node_fill_color + \
            '{%s,%s,%s}' % (str(node_color[0]), str(
                node_color[1]), str(node_color[2])) + '\n'

        text_fill_color = '\\definecolor{%s}{RGB}' % (node['id']+'text')
        text_hex = node['text_color'].lstrip('#')
        text_color = tuple(int(text_hex[i:i+2], 16) for i in (0, 2, 4))
        tcolor = text_fill_color + \
            '{%s,%s,%s}' % (str(text_color[0]), str(
                text_color[1]), str(text_color[2])) + '\n'

        return ncolor, tcolor

    def drawTikzgraph(self, max_xe, min_xe, max_ye, min_ye, node_list, edge_list):
        '''Function for generation Tikz code from parsed .graphml files.
        '''
        if len(max_xe) != 0 and len(max_ye) != 0:
            max_x = max(max([x['x'] for x in node_list]),
                        max([x for x in max_xe]))
            max_y = max(max([y['y'] for y in node_list]),
                        max([y for y in max_ye]))
            min_x = min(min([x['x'] for x in node_list]),
                        min([x for x in min_xe]))
            min_y = min(min([y['y'] for y in node_list]),
                        min([y for y in min_ye]))
        else:
            max_x = max([x['x'] for x in node_list])
            max_y = max([y['y'] for y in node_list])
            min_x = min([x['x'] for x in node_list])
            min_y = min([y['y'] for y in node_list])

        with open(self.file_output, 'w') as out:
            out.write(
                '\\begin{tikzpicture}[rotate=0,scale=' + str(4) + ',font=\\sffamily]' + '\n')

            if self.flag == 'simple':
                if node_list:
                    temp = node_list[0]['id']
                    width = round(float(node_list[0]['thick']) * 0.4, 2)
                    node_list[0]['id'] = 'def_node_'
                    ncolor, tcolor, bcolor = self.getAllColors(node_list[0])
                    node_list[0]['id'] = temp
                    out.write('\n'+ncolor)
                    out.write(tcolor)
                    out.write(bcolor)
                    out.write(
                        '\\tikzstyle{default_node_style}=[draw=def_node_draw,fill=def_node_fill,text=def_node_text,line width = %spt]\n\n' % (width))

                if edge_list:
                    temp = edge_list[0]['id']
                    width = round(float(edge_list[0]['thick']) * 0.4, 2)
                    edge_list[0]['id'] = 'def_edge_'
                    ncolor, tcolor = self.getEdgeColors(edge_list[0])
                    edge_list[0]['id'] = temp
                    out.write(ncolor)
                    out.write(tcolor)
                    out.write(
                        '\\tikzstyle{default_edge_style}=[draw=def_edge_draw,text=def_edge_text, line width = %spt]\n\n' % (width))

            else:
                out.write('\n')

            if node_list:
                for node in node_list:
                    self.drawNode(max_x, max_y, min_x, min_y, out, node)

            if edge_list:
                for edge in edge_list:
                    label = ''
                    if self.flag == 'simple':
                        label = edge['label']
                    elif self.flag == 'advanced':
                        if edge['label'] != '':
                            fontsize = '\\fontsize{7}{14.4}\\selectfont'
                            if edge['labelfontstyle'] == 'plain':
                                label = fontsize + ' ' + edge['label']
                            elif edge['labelfontstyle'] == 'bold':
                                label = fontsize + ' ' + \
                                    '\\textbf{' + edge['label'] + '}'
                            elif edge['labelfontstyle'] == 'italic':
                                label = fontsize + ' ' + \
                                    '\\textit{' + edge['label'] + '}'
                            elif edge['labelfontstyle'] == 'bolditalic':
                                label = fontsize + ' ' + \
                                    '\\textit{\\textbf{' + \
                                    edge['label'] + '}' + '}'
                    if edge['source'] == edge['target']:
                        self.drawDefEdge(max_x, max_y, min_x,
                                         min_y, out, edge, label)
                    elif edge['polyedge'] == True:
                        self.drawPolyLine(max_x, max_y, min_x,
                                          min_y, out, edge, label)
                    elif edge['arcedge'] == True:
                        self.drawArcEdge(max_x, max_y, min_x,
                                         min_y, out, edge, label)
                    elif edge['bezedge'] == True:
                        self.drawBezEdge(max_x, max_y, min_x,
                                         min_y, out, edge, label)
                    elif edge['spledge'] == True:
                        self.drawSpliEdge(max_x, max_y, min_x,
                                          min_y, out, edge, label)
                    else:
                        self.drawDefEdge(max_x, max_y, min_x,
                                         min_y, out, edge, label)

            out.write('\n\\end{tikzpicture}')
            out.close()
            return open(self.file_output, 'r').read()

    def drawNode(self, max_x, max_y, min_x, min_y, out, node):
        x, y = self.normalize(node['x'], node['y'], max_x, max_y, min_x, min_y)
        try:
            shape = self.shape_dict[node['shape']]
        except:
            shape = 'circle'
        if node['height'] != node['width'] and self.shape_dict[node['shape']] == 'circle':
            height = round(float(0.2*float(node['height']))/float(30),2)
            width = round(float(0.2*float(node['width']))/float(30),2)
            shape = 'ellipse, minimum height=%scm ,minimum width=%scm' % (height,width)
        if self.flag == 'simple':
            if node['label'] == '':
                out.write('\\node(%s) at (%s,-%s) [%s,default_node_style] {%s};\n\n'
                          % (node['id'], str(x), str(y), shape, node['label']))
            else:
                out.write('\\node(%s) at (%s,-%s) [%s,default_node_style] {%s};\n\n'
                          % (node['label'], str(x), str(y), shape,
                             node['label']))

        elif self.flag == 'advanced':
            ncolor, tcolor, bcolor = self.getAllColors(node)
            out.write(ncolor)
            out.write(tcolor)
            out.write(bcolor)
            width = round(float(node['thick']) * 0.4, 2)
            if node['label'] == '':
                out.write('\\node(%s) at (%s,-%s) [%s, draw=%s, fill=%s, text=%s, line width = %spt] {%s};\n\n'
                          % (node['id'], str(x), str(y), shape,
                             node['id']+'draw', node['id']+'fill', node['id']+'text', width, node['label']))
            else:
                fontsize = '\\fontsize{7}{14.4}\\selectfont'
                if node['labelfontstyle'] == 'plain':
                    label = fontsize + ' ' + node['label']
                elif node['labelfontstyle'] == 'bold':
                    label = fontsize + ' ' + '\\textbf{' + node['label'] + '}'
                elif node['labelfontstyle'] == 'italic':
                    label = fontsize + ' ' + '\\textit{' + node['label'] + '}'
                elif node['labelfontstyle'] == 'bolditalic':
                    label = fontsize + ' ' + \
                        '\\textit{\\textbf{' + node['label'] + '}' + '}'
                out.write('\\node(%s) at (%s,-%s) [%s, draw=%s, fill=%s, text=%s, line width = %spt] {%s};\n\n'
                          % (node['label'], str(x), str(y), shape,
                             node['id']+'draw', node['id']+'fill', node['id']+'text', width, label))

    def drawPolyLine(self, max_x, max_y, min_x, min_y, out, edge, label):
        if self.flag == 'simple':
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,default_edge_style]')
            else:
                out.write('\\draw[default_edge_style]')
            if edge['pclist'] == True:
                path = ''
                for point in edge['clist']:
                    x, y = self.normalize(float(point[0]), float(
                        point[1]), max_x, max_y, min_x, min_y)
                    path = path + '(' + str(x) + ',-' + str(y) + ')' + '--'
                if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                    out.write('(%s) -- %s (%s) node[above] {%s}' %
                              (edge['source'], path, edge['target'], label))
                elif self.label_dict[edge['source']] == '':
                    out.write('(%s) -- %s (%s) node[above] {%s}' %
                              (edge['source'], path, self.label_dict[edge['target']], label))
                elif self.label_dict[edge['target']] == '':
                    out.write('(%s) -- %s (%s) node[above] {%s}' %
                              (self.label_dict[edge['source']], path, edge['target'], label))
                else:
                    out.write('(%s) -- %s (%s) node[above] {%s}' % (
                        self.label_dict[edge['source']], path, self.label_dict[edge['target']], label))

                out.write(';' + '\n')
            else:
                if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                    out.write('(%s) edge node[above] {%s} (%s)' %
                              (edge['source'], label, edge['target']))
                elif self.label_dict[edge['source']] == '':
                    out.write('(%s) edge node[above] {%s} (%s)' %
                              (edge['source'], label, self.label_dict[edge['target']]))
                elif self.label_dict[edge['target']] == '':
                    out.write('(%s) edge node[above] {%s} (%s)' %
                              (self.label_dict[edge['source']], label, edge['target']))
                else:
                    out.write('(%s) edge node[above] {%s} (%s)' % (
                        self.label_dict[edge['source']], label, self.label_dict[edge['target']]))
                out.write(';' + '\n')

        else:
            ncolor, tcolor = self.getEdgeColors(edge)
            out.write('\n'+ncolor)
            out.write(tcolor)
            width = round(float(edge['thick']) * 0.4, 2)
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text',width))
            else:
                out.write('\\draw[draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text', width))
            if edge['pclist'] == True:
                path = ''
                for point in edge['clist']:
                    x, y = self.normalize(float(point[0]), float(
                        point[1]), max_x, max_y, min_x, min_y)
                    path = path + '(' + str(x) + ',-' + str(y) + ')' + '--'
                if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                    out.write('(%s) -- %s (%s) node[above] {%s}' %
                              (edge['source'], path, edge['target'], label))
                elif self.label_dict[edge['source']] == '':
                    out.write('(%s) -- %s (%s) node[above] {%s}' %
                              (edge['source'], path, self.label_dict[edge['target']], label))
                elif self.label_dict[edge['target']] == '':
                    out.write('(%s) -- %s (%s) node[above] {%s}' %
                              (self.label_dict[edge['source']], path, edge['target'], label))
                else:
                    out.write('(%s) -- %s (%s) node[above] {%s}' % (
                        self.label_dict[edge['source']], path, self.label_dict[edge['target']], label))

                out.write(';' + '\n')
            else:
                if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                    out.write('(%s) edge node[above] {%s} (%s)' %
                              (edge['source'], label, edge['target']))
                elif self.label_dict[edge['source']] == '':
                    out.write('(%s) edge node[above] {%s} (%s)' %
                              (edge['source'], label, self.label_dict[edge['target']]))
                elif self.label_dict[edge['target']] == '':
                    out.write('(%s) edge node[above] {%s} (%s)' %
                              (self.label_dict[edge['source']], label, edge['target']))
                else:
                    out.write('(%s) edge node[above] {%s} (%s)' % (
                        self.label_dict[edge['source']], label, self.label_dict[edge['target']]))
                out.write(';' + '\n')

    def drawArcEdge(self, max_x, max_y, min_x, min_y, out, edge, label):

        if self.flag == 'simple':
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,default_edge_style]')
            else:
                out.write('\\draw[default_edge_style]')

            if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                out.write('(%s) edge[bend left] node[above] {%s} (%s)' %
                          (edge['source'], label, edge['target']))
            elif self.label_dict[edge['source']] == '':
                out.write('(%s) edge[bend left] node[above] {%s} (%s)' %
                          (edge['source'], label, self.label_dict[edge['target']]))
            elif self.label_dict[edge['target']] == '':
                out.write('(%s) edge[bend left] node[above] {%s} (%s)' %
                          (self.label_dict[edge['source']], label, edge['target']))
            else:
                out.write('(%s) edge[bend left] node[above] {%s} (%s)' % (
                    self.label_dict[edge['source']], label, self.label_dict[edge['target']]))

        else:
            ncolor, tcolor = self.getEdgeColors(edge)
            out.write('\n'+ncolor)
            out.write(tcolor)
            width = round(float(edge['thick']) * 0.4, 2)
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text',width))
            else:
                out.write('\\draw[draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text',width))

            if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                out.write('(%s) edge[bend left] node[above] {%s} (%s)' %
                          (edge['source'], label, edge['target']))
            elif self.label_dict[edge['source']] == '':
                out.write('(%s) edge[bend left] node[above] {%s} (%s)' %
                          (edge['source'], label, self.label_dict[edge['target']]))
            elif self.label_dict[edge['target']] == '':
                out.write('(%s) edge[bend left] node[above] {%s} (%s)' %
                          (self.label_dict[edge['source']], label, edge['target']))
            else:
                out.write('(%s) edge[bend left] node[above] {%s} (%s)' % (
                    self.label_dict[edge['source']], label, self.label_dict[edge['target']]))

        out.write(';' + '\n')

    def drawBezEdge(self, max_x, max_y, min_x, min_y, out, edge, label):
        if self.flag == 'simple':
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,default_edge_style]')
            else:
                out.write('\\draw[default_edge_style]')

            path = 'controls '
            counter = 0
            if len(edge['clist']) == 1:
                for point in edge['clist']:
                    x, y = self.normalize(float(point[0]), float(
                        point[1]), max_x, max_y, min_x, min_y)
                    path = path + '(' + str(x) + ',-' + str(y) + ')'
            else:
                for point in edge['clist']:
                    if counter < 2:
                        x, y = self.normalize(float(point[0]), float(
                            point[1]), max_x, max_y, min_x, min_y)
                        path = path + '(' + str(x) + ',-' + str(y) + ')'
                        counter = counter + 1
                        if len(edge['clist']) == 1:
                            break
                        if counter < 2:
                            path = path + ' and '
            if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                out.write('(%s) .. %s .. node[above] {%s} (%s)' %
                          (edge['source'], path, label, edge['target']))
            elif self.label_dict[edge['source']] == '':
                out.write('(%s) .. %s .. node[above] {%s} (%s)' %
                          (edge['source'], path, label, self.label_dict[edge['target']]))
            elif self.label_dict[edge['target']] == '':
                out.write('(%s) .. %s .. node[above] {%s} (%s)' %
                          (self.label_dict[edge['source']], path, label, edge['target']))
            else:
                out.write('(%s) .. %s .. node[above] {%s} (%s)' % (
                    self.label_dict[edge['source']], path, label, self.label_dict[edge['target']]))

        else:
            ncolor, tcolor = self.getEdgeColors(edge)
            out.write('\n'+ncolor)
            out.write(tcolor)
            width = round(float(edge['thick']) * 0.4, 2)
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text',width))
            else:
                out.write('\\draw[draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text',width))

            path = 'controls '
            counter = 0
            if len(edge['clist']) == 1:
                for point in edge['clist']:
                    x, y = self.normalize(float(point[0]), float(
                        point[1]), max_x, max_y, min_x, min_y)
                    path = path + '(' + str(x) + ',-' + str(y) + ')'
            else:
                for point in edge['clist']:
                    if counter < 2:
                        x, y = self.normalize(float(point[0]), float(
                            point[1]), max_x, max_y, min_x, min_y)
                        path = path + '(' + str(x) + ',-' + str(y) + ')'
                        counter = counter + 1
                        if len(edge['clist']) == 1:
                            break
                        if counter < 2:
                            path = path + ' and '
            if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                out.write('(%s) .. %s .. node[above] {%s} (%s)' %
                          (edge['source'], path, label, edge['target']))
            elif self.label_dict[edge['source']] == '':
                out.write('(%s) .. %s .. node[above] {%s} (%s)' %
                          (edge['source'], path, label, self.label_dict[edge['target']]))
            elif self.label_dict[edge['target']] == '':
                out.write('(%s) .. %s .. node[above] {%s} (%s)' %
                          (self.label_dict[edge['source']], path, label, edge['target']))
            else:
                out.write('(%s) .. %s .. node[above] {%s} (%s)' % (
                    self.label_dict[edge['source']], path, label, self.label_dict[edge['target']]))

        out.write(';' + '\n')

    def drawSpliEdge(self, max_x, max_y, min_x, min_y, out, edge, label):
        if self.flag == 'simple':
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,default_edge_style]')
            else:
                out.write('\\draw[default_edge_style]')

            path = ''
            if len(edge['clist']) == 1:
                for point in edge['clist']:
                    x, y = self.normalize(float(point[0]), float(
                        point[1]), max_x, max_y, min_x, min_y)
                    path = path + '(' + str(x) + ',-' + str(y) + ')'
            else:
                for point in edge['clist']:
                    x, y = self.normalize(float(point[0]), float(
                        point[1]), max_x, max_y, min_x, min_y)
                    path = path + '(' + str(x) + ',-' + str(y) + ') '

            if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                out.write('plot[smooth] coordinates {(%s) %s (%s)} node[above] {%s}' %
                          (edge['source'], path, edge['target'], label))
            elif self.label_dict[edge['source']] == '':
                out.write('plot[smooth] coordinates {(%s) %s (%s)} node[above] {%s}' %
                          (edge['source'], path, self.label_dict[edge['target']], label))
            elif self.label_dict[edge['target']] == '':
                out.write('plot[smooth] coordinates {(%s) %s (%s)} node[above] {%s}' %
                          (self.label_dict[edge['source']], path, edge['target'], label))
            else:
                out.write('plot[smooth] coordinates {(%s) %s (%s)} node[above] {%s}' % (
                    self.label_dict[edge['source']], path, self.label_dict[edge['target']], label))

        else:
            ncolor, tcolor = self.getEdgeColors(edge)
            out.write('\n'+ncolor)
            out.write(tcolor)
            width = round(float(edge['thick']) * 0.4, 2)
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text',width))
            else:
                out.write('\\draw[draw =%s,text=%s] ' %
                          (edge['id']+'draw', edge['id']+'text'))

            path = ''
            if len(edge['clist']) == 1:
                for point in edge['clist']:
                    x, y = self.normalize(float(point[0]), float(
                        point[1]), max_x, max_y, min_x, min_y)
                    path = path + '(' + str(x) + ',-' + str(y) + ')'
            else:
                for point in edge['clist']:
                    x, y = self.normalize(float(point[0]), float(
                        point[1]), max_x, max_y, min_x, min_y)
                    path = path + '(' + str(x) + ',-' + str(y) + ') '

            if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                out.write('plot[smooth] coordinates {(%s) %s (%s)} node[above] {%s}' %
                          (edge['source'], path, edge['target'], label))
            elif self.label_dict[edge['source']] == '':
                out.write('plot[smooth] coordinates {(%s) %s (%s)} node[above] {%s}' %
                          (edge['source'], path, self.label_dict[edge['target']], label))
            elif self.label_dict[edge['target']] == '':
                out.write('plot[smooth] coordinates {(%s) %s (%s)} node[above] {%s}' %
                          (self.label_dict[edge['source']], path, edge['target'], label))
            else:
                out.write('plot[smooth] coordinates {(%s) %s (%s)} node[above] {%s}' % (
                    self.label_dict[edge['source']], path, self.label_dict[edge['target']], label))

        out.write(';' + '\n')

    def drawDefEdge(self, max_x, max_y, min_x, min_y, out, edge, label):
        if self.flag == 'simple':
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,default_edge_style]')
            else:
                out.write('\\draw[default_edge_style]')

            if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                out.write('(%s) edge node[above] {%s} (%s)' %
                          (edge['source'], label, edge['target']))
            elif self.label_dict[edge['source']] == '':
                out.write('(%s) edge node[above] {%s} (%s)' %
                          (edge['source'], label, self.label_dict[edge['target']]))
            elif self.label_dict[edge['target']] == '':
                out.write('(%s) edge node[above] {%s} (%s)' %
                          (self.label_dict[edge['source']], label, edge['target']))
            else:
                out.write('(%s) edge node[above] {%s} (%s)' % (
                    self.label_dict[edge['source']], label, self.label_dict[edge['target']]))

        else:
            ncolor, tcolor = self.getEdgeColors(edge)
            out.write('\n'+ncolor)
            out.write(tcolor)
            width = round(float(edge['thick']) * 0.4, 2)
            if (self.arrow_dict[edge['directed']]) == True:
                out.write('\\draw[->,draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text',width))
            else:
                out.write('\\draw[draw =%s,text=%s,line width = %spt] ' %
                          (edge['id']+'draw', edge['id']+'text',width))

            if self.label_dict[edge['source']] == '' and self.label_dict[edge['target']] == '':
                out.write('(%s) edge node[above] {%s} (%s)' %
                          (edge['source'], label, edge['target']))
            elif self.label_dict[edge['source']] == '':
                out.write('(%s) edge node[above] {%s} (%s)' %
                          (edge['source'], label, self.label_dict[edge['target']]))
            elif self.label_dict[edge['target']] == '':
                out.write('(%s) edge node[above] {%s} (%s)' %
                          (self.label_dict[edge['source']], label, edge['target']))
            else:
                out.write('(%s) edge node[above] {%s} (%s)' % (
                    self.label_dict[edge['source']], label, self.label_dict[edge['target']]))

        out.write(';' + '\n')
