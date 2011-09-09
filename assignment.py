#!/usr/bin/python
# -*- coding: utf-8 -*-

# Functions for simulation of project duration
# -----------------------------------------------------------------------
# PPC-PROJECT
#   Multiplatform software tool for education and research in
#   project management
#
# Copyright 2007-9 Universidad de Córdoba
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

import random
import math

# Internationalization
import gettext
APP = 'PPC-Project'  # Program name
DIR = 'po'  # Directory containing translations, usually /usr/share/locale
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

def datosBetaMedia(mean, k):
    """
    Devuelve los paramentros de la beta basándose únicamente en la media
    y en el valor de proporcionalidad de la desviación típica

    Valores que devuelve: (media, desviación típica, shape factor a, shape factor b)
    """

    stdev = (k*mean) 
    mode = random.uniform(mean*(1-k),mean*(1+k))
    print mode
    op = ((3*mean*(1-k))-(2*mode))
    pes = (op+(6*k*mean))

    return (op, mode, pes, stdev)

def datosTriangularMedia(mean,k):
    """
    Generates a random number in a triangular distribution in [op,pes]
    with mean
    """
    stdev = (k*mean)
    mode = random.uniform(mean*(1-(k*math.sqrt(2))),mean*(1+(k*math.sqrt(2))))
    print mode
    op = ((3*mean-mode)-math.sqrt(pow((3*mean-mode),2)-4*(-3*mean*mode+pow(mode,2)+6*pow(mean,2)*(0.5-pow(0.2,2)))))/2
    pes = 3*mean-op-mode

    return (op, mode, pes, stdev)

def datosUniformeMedia(mean,k):
    """
    Generates a random number in a Uniform distribution having only the mean.
    """
    stdev = (k*mean)
    op = mean * (1-(k* math.sqrt(3)))
    pes = mean * (1+(k* math.sqrt(3)))
    mode = (op + pes) / 2

    return (op, pes, stdev, mode)

def datosNormalMedia(mean,k):
    """
    Generates a number from a Normal random variate with mean and stdev
    """

    stdev = k*mean

    return stdev

def actualizarInterfaz (modelo, k, dist,actividad):

        for m in range(len(actividad)):
            actividad [m][8] = dist
            modelo [m][8] = str(dist)
        
        # Se comprueba el tipo de distribucion y se le asignan los valores
        if dist == 'Uniforme':
            for m in range(len(actividad)):                
                actividad [m][3], actividad[m][5],actividad[m][7], actividad [m][4] = datosUniformeMedia(actividad[m][6], k)
                modelo [m][3], modelo[m][5],modelo[m][7], modelo[m][4] = float(actividad [m][3]), float(actividad[m][5]), float(actividad[m][7]), float(actividad[m][4])
        elif dist == 'Beta':
            for m in range(len(actividad)):
                actividad [m][3], actividad [m][4], actividad[m][5], actividad[m][7] = datosBetaMedia(actividad[m] [6], k)
                modelo [m][3], modelo[m][4],modelo[m][5],modelo[m][7] = actividad [m][3], actividad[m][4], actividad[m][5], actividad[m][7]
        elif dist == 'Triangular':
            for m in range(len(actividad)):
                actividad[m][3], actividad[m][4], actividad[m][5], actividad[m][7] = datosTriangularMedia(actividad[m][6], k)
                modelo [m][3], modelo[m][4],modelo[m][5],modelo[m][7] = actividad [m][3], actividad[m][4], actividad[m][5], actividad[m][7]
        else:
            for m in range(len(actividad)):
                actividad[m][7] = datosNormalMedia(actividad[m][6], k)
                modelo[m][7] = actividad[m][7]

        return modelo, actividad
        


