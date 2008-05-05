#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gantt diagram drawing GTK widget
#-----------------------------------------------------------------------
# PPC-PROJECT
#   Multiplatform software tool for education and research in 
#   project management
#
# Copyright 2007-8 Universidad de Córdoba
# This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published
#   by the Free Software Foundation, either version 3 of the License,
#   or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cairo
import math
import gtk
import gtk.gdk
import gobject

class GTKgantt(gtk.VBox):
    """
    Class GTKgantt
        Structure:
            GTKgantt(gtk.VBox)
                GanttHeader(gtk.Layout)
                gtk.ScrolledWindow
                    GanttDrawing

        Properties:
            header
            diagram
            scrolled_window

        Interface:
            set_vadjustment(adjustment)
            set_hadjustment(adjustment)
            set_policy(horizontal policy, vertical policy)
            set_cell_width(width)
            set_header_height(height)
            set_row_height(height)
            update()
            add_activity(name, prelations, duration = 0 , start_time = 0, slack = 0, comment = "")
            rename_activity(old name, new name)
            set_activity_duration(activity, duration)
            set_activity_prelations(activity, prelations)
            set_activity_slack(activity, slack)
            set_activity_start_time(activity, time)
            set_activity_comment(activity, comment)
            set_activities_color(color)
            set_slack_color(color)
            set_thin_slack(value)
            remove_activity(activity)
            reorder(activities)
            show_arrows(value)
            clear()
    """
    def __init__(self):
        gtk.VBox.__init__(self)
        #Creating objects
        self.header = GanttHeader()
        self.diagram = GanttDrawing()
        #Setting adjustments
        self.diagram.set_hadjustment(self.header.get_hadjustment())
        self.scrolled_window = gtk.ScrolledWindow(self.diagram.get_hadjustment(), self.diagram.get_vadjustment())
        #Packing
        self.set_homogeneous(False)
        self.pack_start(self.header, False, False, 0)
        self.pack_start(self.scrolled_window, True, True, 0)
        self.scrolled_window.add(self.diagram)
        #Setting scrollbars policy
        self.scrolled_window.set_policy(gtk.POLICY_ALWAYS,gtk.POLICY_AUTOMATIC)
        #Setting minimum size
        self.set_size_request(100,100)
        #Connecting signals
        self.diagram.connect("gantt-width-changed", self.header.set_width)
    def set_vadjustment(self, adjustment):
        """
        Set vertical adjustment to "adjustment"
        
        adjustment: gtk.Adjustment to be set.
        """
        self.diagram.set_vadjustment(adjustment)
    def set_hadjustment(self, adjustment):
        """
        Set horizontal adjustment to "adjustment"
        
        adjustment: gtk.Adjustment to be set.
        """
        self.diagram.set_hadjustment(adjustment)
        self.header.set_hadjustment(adjustment)
    def set_policy(self, hpol, vpol):
        """
        Set scrollbars policy
        
        hpol: horizontal policy (gtk.POLICY_ALWAYS, gtk.POLICY_AUTOMATIC or gtk.POLICY_NEVER)
        vpol: vertical policy (gtk.POLICY_ALWAYS, gtk.POLICY_AUTOMATIC or gtk.POLICY_NEVER)
        """
        self.scrolled_window.set_policy(hpol , vpol)
    def set_cell_width(self, num):
        """
        Set cell width
        
        num: width (pixels)
        """
        self.header.set_cell_width(num)
        self.diagram.set_cell_width(num)
    def set_row_height(self,num):
        """
        Set row height
        
        num: height (pixels)
        """
        self.diagram.set_row_height(num)
    def set_header_height(self,num):
        """
        Set header height
        
        num: height (pixels)
        """
        self.header.set_height(num)
    def update(self):
        """
        Redraw Gantt diagram.
        
        """
        self.diagram.queue_draw()
        self.header.queue_draw()
    def add_activity(self, name, prelations=[], duration = 0, start_time = 0, slack = 0, comment = ""):
        """
        Add an activity to the diagram
        
        name: Activity name (string)
        prelations: List of strings containing activity names.
        duration: duration of the activity measured in units of time.
        start_time: unit of time when the activity start.
        slack: slack measured in units of time.
        comment: String that will be shown to the right of the activity (string).
        """
        self.diagram.add_activity(name, prelations, duration, start_time, slack, comment)
    def rename_activity(self,old,new):
        """
        Changes the name of an activity.

        old: old name (string)
        new: new name (string)
        """
        if (old != new):
            self.diagram.set_activity_name(old,new)
    def set_activity_duration(self, activity, duration):
        """
        Change the duration of an activity

        activity: name of the activity (string)
        duration: duration of the activity measured in units of time.
        """
        self.diagram.set_activity_duration(activity,duration)
    def set_activity_prelations(self,activity,prelations):
        """
        Change the prelations of an activity

        activity: name of the activity (string)
        prelations: List of strings containing activity names.
        """
        self.diagram.set_activity_prelations(activity,prelations)
    def set_activity_slack(self,activity,slack):
        """
        Change the slack of an activity

        activity: name of the activity (string)
        slack: slack measured in units of time
        """
        self.diagram.set_activity_slack(activity,slack)
    def set_activity_comment(self,activity,comment):
        """
        Change the comment of an activity

        activity: name of the activity (string)
        comment: String that will be shown to the right of the activity (string)
        """
        self.diagram.set_activity_comment(activity,comment)
    def set_activity_start_time(self,activity,time):
        """
        Change the start time of an activity

        activity: name of the activity (string)
        time: unit of time when the activity start.
        """
        self.diagram.set_activity_start_time(activity,time)
    def set_activities_color(self, color):
        """
        Change the color of the activities rectangles

        color: new color (gtk.gdk.Color)
        """
        self.diagram.set_activities_color(color)
    def set_slack_color(self, color):
        """
        Change the color of the slacks rectangles

        color: new color (gtk.gdk.Color)
        """
        self.diagram.set_slack_color(color)
    def set_thin_slack(self, value):
        """
        Set if the slacks rectangles will be thinner than the activities ones

        value (True or False)
        """
        self.diagram.set_thin_slack(value)
    def remove_activity(self, activity):
        """
        Removes an activity from the diagram.

        activity: name of the activity (string)
        """
        self.diagram.remove_activity(activity)
    def reorder(self,activities):
        """
        change the order of the activities
        
        activities: list of strings containing activity names.
        """
        self.diagram.reorder(activities)
    def show_arrows(self, value):
        """
        Set if the prelation arrows should be shown or not.

        value (True or False)
        """
        self.diagram.show_arrows(value)
    def clear(self):
        """
        Clear all the activities information
        """
        self.diagram.clear()
        self.header.set_width(None, 0)

class GanttHeader(gtk.Layout):
    """    
    Class GanttHeader

        Properties:
            width
            cell_width
            height
            context
            available_width

        Interface:
            set_cell_width(width)
            set_width(width)
            set_height(height)
            expose(widget,event)
            draw(context)
    """
    def __init__(self):
        gtk.Layout.__init__(self)
        #Initialising values
        self.width = self.cell_width = 25
        self.height = 28
        #Connecting signals
        self.connect("expose-event", self.expose)
        #Setting size request
        self.set_size_request(self.width, self.height)
    def set_cell_width(self,num):
        """
        Set cell width
        
        num: width (pixels)
        """
        self.cell_width = num
    def set_width(self, widget, width):
        """
        Set header width.
        
        widget
        width: width (pixels)
        """
        self.width = width
        self.set_size_request(width, self.height)
    def set_height(self, num):
        """
        Set header height
        
        num: height (pixels)
        """
        self.height = num
        self.set_size_request(self.width, self.height)
    def expose (self,widget,event):
        """
        Function called when the widget needs to be drawn
        
        widget:
        event:

        Returns: False
        """
        #Creating Cairo drawing context
        self.context = self.bin_window.cairo_create()
        #Setting context size to available size
        self.context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        self.context.clip()
        #Obtaining available width
        self.available_width = event.area.width
        #Drawing
        self.draw(self.context)
        return False
    def draw(self, context):
        """
        Draw the widget

        context: Cairo context (gtk.gdk.CairoContext)
        """
        #Setting Layout size
        self.set_size(self.width + self.cell_width, self.height) #An extra cell is needed in case the diagram vertical scrollbar is visible
        #Drawing cells with numbers inside
        context.translate(0.5, 0.5)
        context.set_source_color(self.get_style().fg[gtk.STATE_NORMAL])
        for i in range(0, max(self.available_width, self.width) / self.cell_width + 1):
            context.rectangle(i * self.cell_width, 0, self.cell_width, self.height - 1)
            x_bearing, y_bearing, txt_width, txt_height = context.text_extents(str(i+1))[:4]
            context.move_to((i + 0.5) * self.cell_width - txt_width / 2 - x_bearing, self.height / 2 - txt_height / 2 - y_bearing )
            context.show_text(str(i+1))
        context.set_line_width(1);
        context.stroke()

class Diagram_graph():
    """
    Class Diagram_graph:
        Simple structure created to group the activities information

        Properties:
            activities: list of string containing activity names
            prelations: dictionary (index: activity names (strings), definitions: List of strings containing activity names).
            duration: dictionary (index: activity names (strings), definitions: duration of the activity measured in units of time).
            start_time: dictionary (index: activity names (strings), definitions: unit of time when the activity start).
            slack: dictionary (index: activity names (strings), definitions: slack measured in units of time).
            comment: dictionary (index: activity names (strings), definitions: string that will be shown to the right of the activity (string))
    """
    activities = []
    durations = {}
    prelations = {}
    start_time = {}
    slacks = {}
    comments = {}

class GanttDrawing(gtk.Layout):
    """
    Class GanttDrawing(gtk.Layout)

        Properties:
            graph
            row_height
            cell_width
            width
            available_width
            modified
            activities_color
            slack_color
            thin_slack
            context
            arrows

        Interface:
            set_policy(horizontal policy, vertical policy)
            set_cell_width(width)
            set_row_height(height)
            update()
            add_activity(name, prelations, duration = 0 , start_time = 0, slack = 0, comment = "")
            rename_activity(old name, new name)
            set_activity_duration(activity, duration)
            set_activity_prelations(activity, prelations)
            set_activity_slack(activity, slack)
            set_activity_start_time(activity, time)
            set_activity_comment(activity, comment)
            set_activities_color(color)
            set_slack_color(color)
            set_thin_slack(value)
            remove_activity(activity)
            reorder(activities)
            show_arrows(value)
            clear()

        Signals:
            'gantt-width-changed' Signal emmited when the required width has changed. Parameters: widget, width
    """
    __gsignals__ = {'gantt-width-changed' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,(gobject.TYPE_INT,))}
    def __init__(self):
        gtk.Layout.__init__(self)
        #Creating objects
        self.graph = Diagram_graph()
        #Initialising values
        self.row_height = 25
        self.cell_width = 25
        self.width = 0
        self.modified = 0
        self.activities_color = None
        self.slack_color = None
        self.thin_slack = True
        self.arrows = True
        #Connecting signals
        self.connect("expose-event", self.expose)

    def set_activities_color(self, color):
        """
        Change the color of the activities rectangles

        color: new color (gtk.gdk.Color)
        """
        self.activities_color = color

    def set_slack_color(self, color):
        """
        Change the color of the slacks rectangles

        color: new color (gtk.gdk.Color)
        """
        self.slack_color = color

    def set_thin_slack(self, value):
        """
        Set if the slacks rectangles will be thinner than the activities ones

        value (True or False)
        """
        self.thin_slack = value

    def set_cell_width(self, width):
        """
        Set cell width
        
        num: width (pixels)
        """
        self.cell_width = width
        self.modified = 1

    def set_row_height(self,num):
        """
        Set row height
        
        num: height (pixels)
        """
        self.row_height = num
        self.set_size_request(self.width ,num)

    def get_needed_length (self, context):
        """
        Calculate needed length

        context: Cairo context (gtk.gdk.CairoContext)

        Returns: length measured in pixels
        """
        lengths = []
        for activity in self.graph.activities:
            x_bearing, y_bearing, txt_width, txt_height = context.text_extents(self.graph.comments[activity])[:4]
            lengths.append( (self.graph.start_time[activity] + self.graph.durations[activity] + self.graph.slacks[activity] + 0.25)* self.cell_width + 0.5 + x_bearing + txt_width)
        return(int(max(lengths)+1))

    def clear(self):
        """
        Clear all the activities information
        """
        self.graph.activities = []
        self.graph.durations = {}
        self.graph.prelations = {}
        self.graph.start_time = {}
        self.graph.slacks = {}
        self.graph.comments = {}

    def add_activity(self, name, prelations, duration, start_time, slack, comment):
        """
        Add an activity to the diagram
        
        name: Activity name (string)
        prelations: List of strings containing activity names.
        duration: duration of the activity measured in units of time.
        start_time: unit of time when the activity start.
        slack: slack measured in units of time.
        comment: String that will be shown to the right of the activity (string).
        """
        if (name != ""):
            self.graph.activities.append(name)
            if (prelations == ""):
                prelations = []
            self.graph.prelations[name] = prelations
            if (duration == ""):
                duration = 0
            self.graph.durations[name] = duration
            if (start_time == ""):
                start_time = 0
            self.graph.start_time[name] = start_time
            if (slack == ""):
                slack = 0
            self.graph.slacks[name] = slack
            self.graph.comments[name] = comment
            self.modified = 1

    def set_activity_name(self,activity,name):
        """
        Changes the name of an activity.

        activity: old name (string)
        name: new name (string)
        """
        self.graph.durations[name] = self.graph.durations[activity]
        del self.graph.durations[activity]
        self.graph.start_time[name] = self.graph.start_time[activity]
        del self.graph.start_time[activity]
        self.graph.slacks[name] = self.graph.slacks[activity]
        del self.graph.slacks[activity]
        self.graph.comments[name] = self.graph.comments[activity]
        del  self.graph.comments[activity]
        for act in self.graph.activities:
            if activity in self.graph.prelations[act]:
                self.graph.prelations[act].remove(activity)
                self.graph.prelations[act].append(name)
        self.graph.prelations[name] = self.graph.prelations[activity]
        del  self.graph.prelations[activity]         
        self.graph.activities[self.graph.activities.index(activity)] = name

    def set_activity_duration(self, activity, duration):
        """
        Change the duration of an activity

        activity: name of the activity (string)
        duration: duration of the activity measured in units of time.
        """
        self.graph.durations[activity] = duration
        self.modified = 1

    def set_activity_prelations(self,activity,prelations):
        """
        Change the prelations of an activity

        activity: name of the activity (string)
        prelations: List of strings containing activity names.
        """
        self.graph.prelations[activity] = prelations

    def set_activity_slack(self,activity,slack):
        """
        Change the slack of an activity

        activity: name of the activity (string)
        slack: slack measured in units of time
        """
        self.graph.slacks[activity] = slack
        self.modified = 1

    def set_activity_comment(self,activity,comment):
        """
        Change the comments of an activity

        activity: name of the activity (string)
        comment: String that will be shown to the right of the activity (string)
        """
        self.graph.comments[activity] = comment
        self.modified = 1

    def set_activity_start_time(self, activity, time):
        """
        Change the start_time of an activity

        activity: name of the activity (string)
        time: unit of time when the activity start.
        """
        self.graph.start_time[activity] = time
        self.modified = 1

    def remove_activity(self, activity):
        """
        Removes an activity from the diagram.

        activity: name of the activity (string)
        """
        if activity in self.graph.activities:
            del self.graph.durations[activity]
            del self.graph.start_time[activity]
            del self.graph.slacks[activity]
            del  self.graph.comments[activity]         
            for act in self.graph.activities:
                if activity in self.graph.prelations[act]:
                    self.graph.prelations[act].remove(activity)
            del  self.graph.prelations[activity]         
            self.graph.activities.remove(activity)
            self.modified = 1

    def reorder(self,activities):
        """
        change the order of the activities
        
        activities: list of strings containing activity names.
        """
        self.graph.activities = activities
        
    def show_arrows(self, value):
        self.arrows = value

    def expose (self,widget,event):
        """
        Function called when the widget needs to be drawn
        
        widget:
        event:

        Returns: False
        """
        #Creating Cairo drawing context
        self.context = self.bin_window.cairo_create()
        #Setting context size to available size
        self.context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        self.context.clip()
        #Obtaining available width
        self.available_width = event.area.width
        self.available_height = event.area.height
        #Drawing
        self.draw(self.context)
        return False

    def draw(self, context):
        """
        Draw the widget

        context: Cairo context (gtk.gdk.CairoContext)
        """
        #Checking if it is necessary to calculate the needed width of the diagram
        if self.graph.activities != [] and self.modified == 1:
            width = self.get_needed_length(context)
            if width != self.width: #If the width has changed...
                self.set_size_request(width, self.row_height)
                self.width = width
                self.emit("gantt-width-changed",width)
                self.modified = 0
        height = self.row_height * len(self.graph.activities)
        self.set_size(self.width, height)
        context.translate(0.5, 0.5)
        #Drawing cell lines
        for i in range(0, max(self.available_width, self.width) / self.cell_width + 1):
            context.move_to(i * self.cell_width, -1)
            context.line_to(i * self.cell_width, max(self.available_height, height, self.get_vadjustment().upper))
        context.set_line_width(1)
        red = float(self.get_style().fg[gtk.STATE_INSENSITIVE].red) / 65535
        green = float(self.get_style().fg[gtk.STATE_INSENSITIVE].green) / 65535
        blue = float(self.get_style().fg[gtk.STATE_INSENSITIVE].blue) / 65535
        context.set_source_rgba(red, green, blue, 0.3)
        context.stroke()
        #Drawing slacks
        for activity in self.graph.activities:
            context.rectangle((self.graph.start_time[activity]+self.graph.durations[activity])* self.cell_width, self.graph.activities.index(activity) * self.row_height, self.graph.slacks[activity] * self.cell_width , ((self.row_height / 4 ) if self.thin_slack == True else self.row_height)  - 1 )
        context.set_line_width(1)
        if self.slack_color != None:
            red = float(self.slack_color.red) / 65535
            green = float(self.slack_color.green) / 65535
            blue = float(self.slack_color.blue) / 65535
        else:
            red = float(self.get_style().bg[gtk.STATE_ACTIVE].red) / 65535
            green = float(self.get_style().bg[gtk.STATE_ACTIVE].green) / 65535
            blue = float(self.get_style().bg[gtk.STATE_ACTIVE].blue) / 65535
        context.set_source_rgba(red, green, blue, 0.5)
        context.fill_preserve()
        context.set_source_color(self.get_style().fg[gtk.STATE_NORMAL])
        context.stroke()
        #Drawing activities and commentaries
        for activity in self.graph.activities:
            context.rectangle(self.graph.start_time[activity]* self.cell_width, self.graph.activities.index(activity) * self.row_height, self.graph.durations[activity] * self.cell_width , self.row_height - 1 )
            x_bearing, y_bearing, txt_width, txt_height = context.text_extents(self.graph.comments[activity])[:4]
            context.move_to((self.graph.start_time[activity] + self.graph.durations[activity] + self.graph.slacks[activity] + 0.25)* self.cell_width + x_bearing, (self.graph.activities.index(activity)+ 0.90) * self.row_height + y_bearing)
            context.show_text(self.graph.comments[activity])
        context.set_line_width(1)
        if self.activities_color != None:
            red = float(self.activities_color.red) / 65535
            green = float(self.activities_color.green) / 65535
            blue = float(self.activities_color.blue) / 65535
        else:
            red = float(self.get_style().bg[gtk.STATE_SELECTED].red) / 65535
            green = float(self.get_style().bg[gtk.STATE_SELECTED].green) / 65535
            blue = float(self.get_style().bg[gtk.STATE_SELECTED].blue) / 65535
        context.set_source_rgba(red, green, blue, 0.5)
        context.fill_preserve()
        context.set_source_color(self.get_style().fg[gtk.STATE_NORMAL])
        context.stroke()
        #Drawing prelation arrows
        if self.arrows:
            for activity in self.graph.activities:
                x = (self.graph.start_time[activity] + self.graph.durations[activity]) * self.cell_width
                y = (self.graph.activities.index(activity) + 0.5) * self.row_height - 1
                context.set_source_color(self.get_style().fg[gtk.STATE_NORMAL])
                for children in self.graph.prelations[activity]:
                    try:
                        id_actividad2 = self.graph.activities.index(children)
                        #Draw a circle at the end of the activity
                        context.arc(x,y, max(self.cell_width, self.row_height) / 8, 0 , 2 * math.pi )
                        context.fill()
                        #draw an vertical line to the children activity row
                        context.move_to(x,y)
                        y2 = ((id_actividad2) * self.row_height - 4) if id_actividad2 > self.graph.activities.index(activity) else ((id_actividad2 + 1) * self.row_height + 3)
                        context.line_to(x, y2 )
                        context.move_to(x,y2)
                        #draw an horizontal line next to the children activity
                        x2 = self.graph.start_time[children] * self.cell_width
                        context.line_to(x2, y2)
                        context.stroke()
                        #draw a triangle
                        v1 = x2 - 3
                        v2 = x2 + 3
                        context.move_to(v1, y2)
                        context.line_to(x2, (self.row_height *  id_actividad2 -1) if y < y2 else (self.row_height * (id_actividad2 + 1)))
                        context.rel_line_to(3, (-3 if y < y2 else 3))
                        context.close_path()
                        context.fill_preserve()
                        context.stroke()
                    except:
                        pass
      
def main():
    """
        Example of use.
    """
    window = gtk.Window()
    gantt = GTKgantt()
    gantt.add_activity("A", ["B", "C"], 5,0, 0, "Initial Activity")
    gantt.add_activity("B", ["D"], 3, 5, 11)
    gantt.add_activity("C", ["D","E","F","G"], 2, 5,  0 , "Critical Activity")
    gantt.add_activity("D", ["J"], 4, 8, 11)
    gantt.add_activity("E", ["J"], 6, 7, 10, "Not so important activity")
    gantt.add_activity("F", ["H"], 3, 7, 15)
    gantt.add_activity("G", ["I"], 9, 7, 0, "Critical Activity")
    gantt.add_activity("H", [], 1, 15, 10)
    gantt.add_activity("I", [], 10, 16, 0, "Final Activity")
    gantt.add_activity("J", ["H"], 2, 13, 10)
    gantt.set_row_height(25)
    gantt.set_header_height(20)
    gantt.set_cell_width(20)
    window.add(gantt)
    window.connect("destroy", gtk.main_quit)
    gantt.update()
    window.show_all()
    gtk.main()

if __name__ == "__main__":
   main()	
