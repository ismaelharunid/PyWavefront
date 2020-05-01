#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, glob
sys.path.append('..')
import ctypes

from collections import Sequence, Iterable

SUPPORTED_ATTRIBUTES = ('meshes', 'mesh')
INCLUDE_ATTRIBUTES = ()
EXCLUDE_ATTRIBUTES = ()

BASEDIR_PATH = os.path.realpath(os.path.dirname(__file__)) + os.path.sep
BODY_FEMALE_OBJ_PATH = BASEDIR_PATH + 'Realistic_White_Female_Low_Poly.obj'


import pywavefront
from pywavefront.material import Material
from pywavefront.mesh import Mesh
from pywavefront.texture import Texture, TextureOptions
from pywavefront.wavefront import Wavefront


import numpy as np

#import pyglet
#from pyglet.gl import *

'''
def wavefront_dump(scene):
  # Iterate vertex data collected in each material
  for name, material in scene.materials.items():
    # Contains the vertex format (string) such as "T2F_N3F_V3F"
    # T2F, C3F, N3F and V3F may appear in this string
    material.vertex_format
    # Contains the vertex list of floats in the format described above
    material.vertices
    # Material properties
    material.diffuse
    material.ambient
    material.texture
'''

'''
[create a window and set up your OpenGl context]
obj = pywavefront.Wavefront('something.obj')

[inside your drawing loop]
visualization.draw(obj)
'''


attr_names = lambda obj: tuple(name for name in dir(obj) if not name.startswith('_'))

def attr_dump(obj, obj_name='<unknown>', indent=2, include=(), exclude=(), prefix=''):
  print('%s%s attributes:' % (prefix, obj_name))
  for name in attr_names(obj):
    if (exclude and name in exclude) or (include and name not in include): continue
    value = getattr(obj, name)
    if callable(value):
      repr_value = value.__name__ + '(...)'
    else:
      repr_value = repr(value)
      l_repr_value = len(repr_value)
      if l_repr_value > 80:
        repr_value = repr_value[:40] + ' ... ' + repr_value[-35:]
    print('%s%s(%r): %s' % (prefix+' '*indent, name, type(value), repr_value))


def objfile_dump(objpath
    , strict=True
    , encoding="iso-8859-1"
    , create_materials=False
    , collect_faces=False
    , parse=True
    , cache=False
    , indent=2
    , include=INCLUDE_ATTRIBUTES, exclude=EXCLUDE_ATTRIBUTES
    , pretty_data=False
    , verbose=0
    , prefix=''):
  print('%sfile %r' % (prefix, objpath))
  wavefront = pywavefront.Wavefront(objpath
      , strict=strict
      , encoding=encoding
      , create_materials=create_materials
      , collect_faces=collect_faces
      , parse=parse
      , cache=cache)
  wavefront_dump(wavefront, 'wavefront', indent, include, exclude, pretty_data, verbose, prefix+' '*indent)


def wavefront_dump(wavefront, attr_name='wavefront'
    , indent=2
    , include=INCLUDE_ATTRIBUTES, exclude=EXCLUDE_ATTRIBUTES
    , pretty_data=False
    , verbose=0
    , prefix=''):
  wavefront_filename = wavefront.file_name
  print('%s%s file_name=%r' % (prefix, attr_name, wavefront_filename))
  meshes, mesh_list = wavefront.meshes, wavefront.mesh_list
  list_dump(mesh_list, 'mesh_list', indent, include, exclude, pretty_data, verbose, prefix+' '*indent)
  meshes_dump(meshes, 'meshes', indent, include, exclude, pretty_data, verbose, prefix+' '*indent)
  if verbose >= 3: attr_dump(wavefront, 'wavefront', indent \
      , include, tuple(exclude) + SUPPORTED_ATTRIBUTES if verbose == 3 else exclude
      , prefix)


def mesh_dump(mesh, attr_name='mesh'
    , indent=2
    , include=INCLUDE_ATTRIBUTES, exclude=EXCLUDE_ATTRIBUTES
    , pretty_data=False
    , verbose=0
    , prefix=''):
  mesh_name = mesh.name
  n_materials, n_faces = len(mesh.materials), len(mesh.faces) if hasattr(mesh, 'faces') else 0
  print('%s%s: name=%r, %d materals, %d faces' \
      % (prefix, attr_name, mesh_name, n_materials, n_faces))
  print('%smaterials: %d materials' \
      % (prefix+' '*indent, n_materials))
  for i in range(n_materials):
    material = mesh.materials[i]
    material_dump(material, 'material[%d]' % (i,), indent
        , include, exclude, pretty_data, verbose, prefix+' '*indent*2)
  if n_faces:
    faces_dump(mesh.faces, 'faces', indent
        , include, exclude, pretty_data, verbose, prefix+' '*indent)
  if verbose >= 3: attr_dump(mesh, 'mesh', indent \
      , include, tuple(exclude) + SUPPORTED_ATTRIBUTES if verbose == 3 else exclude
      , prefix)


def material_dump(material, attr_name='material'
    , indent=2
    , include=INCLUDE_ATTRIBUTES, exclude=EXCLUDE_ATTRIBUTES
    , pretty_data=False
    , verbose=0
    , prefix=''):
  material_name = material.name
  vertex_format, vertices = material.vertex_format, material.vertices
  n_vertices, vertex_size = len(material.vertices), material.vertex_size
  if not isinstance(vertices[0], Iterable):
    assert 0 == len(material.vertices) % vertex_size \
        , 'incorrect vertex_size(%d) for %d vertices' \
        % (vertex_size, n_vertices)
    vertices = tuple(vertices[i:i+vertex_size] for i in range(0, len(material.vertices), vertex_size))
    n_vertices = len(vertices)
  print('%s%s: name=%s, %d vertices[%s]' \
      % (prefix, attr_name, material_name, n_vertices, vertex_format))
  vertices_dump(vertices, 'vertices', indent
        , include, exclude, pretty_data, verbose, prefix+' '*indent)
  if verbose >= 3: attr_dump(material, 'material', indent \
      , include, tuple(exclude) + SUPPORTED_ATTRIBUTES if verbose == 3 else exclude
      , prefix)


def faces_dump(faces, attr_name='faces'
    , indent=2
    , include=INCLUDE_ATTRIBUTES, exclude=EXCLUDE_ATTRIBUTES
    , pretty_data=False
    , verbose=0
    , prefix=''):
  n_faces = len(faces)
  print('%s%s: %d faces' \
      % (prefix, attr_name, n_faces))
  for i in range(n_faces):
    face = faces[i]
    print('%s%s[%d]: %r' \
        % (prefix+' '*indent, attr_name, i, face))


def vertices_dump(vertices, attr_name='vertices'
    , indent=2
    , include=INCLUDE_ATTRIBUTES, exclude=EXCLUDE_ATTRIBUTES
    , pretty_data=False
    , verbose=0
    , prefix=''):
  n_vertices = len(vertices)
  print('%s%s: %d vertices' \
      % (prefix, attr_name, n_vertices))
  for i in range(n_vertices):
    vertice = vertices[i]
    print('%s%s[%d]: %r' \
        % (prefix+' '*indent, attr_name, i, vertice))


DUMP_PLUGINS = \
    { Mesh: mesh_dump
    , Material: material_dump
    , Wavefront: wavefront_dump
#    , Texture: texture_dump
#    , TextureOptions: textureoptions_dump
    }
def list_dump(list_object, attr_name='list'
    , indent=2
    , include=INCLUDE_ATTRIBUTES
    , exclude=EXCLUDE_ATTRIBUTES
    , pretty_data=False
    , verbose=0
    , prefix=''):
  assert isinstance(list_object, Sequence), 'error: list_dump requires an object with a Sequence interface'
  n_list_object = len(list_object)
  print('%s%s: %d items' \
      % (prefix, attr_name, n_list_object))
  for i in range(n_list_object):
    sub_name = '%s[%d]' % (attr_name, i)
    item = list_object[i]
    item_type = type(item)
    if item_type in DUMP_PLUGINS:
      DUMP_PLUGINS[item_type](item, sub_name \
          , indent \
          , include \
          , tuple(exclude) + SUPPORTED_ATTRIBUTES if verbose == 3 else exclude \
          , pretty_data \
          , verbose \
          , prefix+' '*indent)
    elif isinstance(item_type, Sequence):
      list_dump(item, sub_name \
          , indent \
          , include
          , tuple(exclude) + SUPPORTED_ATTRIBUTES if verbose == 3 else exclude \
          , pretty_data \
          , verbose \
          , prefix+' '*indent)
    else:
      print('%s%s(%r): %r' % (prefix+' '*indent, sub_name, item_type, item))


def meshes_dump(meshes, attr_name='meshes', indent=2
    , include=INCLUDE_ATTRIBUTES, exclude=EXCLUDE_ATTRIBUTES
    , pretty_data=False
    , verbose=0
    , prefix=''):
  n_meshes = len(meshes)
  print('%s%s: %d meshes' \
      % (prefix, attr_name, n_meshes))
  for (mesh_name, mesh) in meshes.items():
    mesh_dump(mesh, 'meshes[%r]' % (mesh_name,), indent
        , include, exclude, pretty_data, verbose, prefix+' '*indent)


def find_obj_files(glob_filter='*.obj', basepath=None, ignore_case=False):
  sep = os.path.sep
  if basepath is None: basepath = os.getcwd()
  if glob_filter.startswith('.'+os.path.sep):
    glob_filter = basepath.rstrip(sep) + glob_filter[1:]
  elif not glob_filter.startswith(sep):
    glob_filter = basepath.rstrip(sep) + sep + glob_filter
  globber = glob.iglob if ignore_case else glob.glob
  return globber(glob_filter)

