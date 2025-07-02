import matplotlib.pyplot as plt
#Instalar previamente: py -m pip install matplotlib_venn
# https://github.com/konstantint/matplotlib-venn
from matplotlib_venn import venn2
from matplotlib_venn.layout.venn2 import DefaultLayoutAlgorithm
import os
from matplotlib.patches import Rectangle


# Ruta para guardar imágenes
carpeta = "graficos"
os.makedirs(carpeta, exist_ok=True)

def limpiar_etiquetas(venn):
    """Elimina texto automático del diagrama."""
    for label in venn.set_labels:
        if label: label.set_text('')
    for label in venn.subset_labels:
        if label: label.set_text('')

def aplicar_estilo(parche, color='white', hatch=None):
    parche.set_facecolor(color)
    parche.set_edgecolor('black')
    parche.set_linewidth(1.5)
    parche.set_alpha(1.0)
    if hatch:
        parche.set_hatch(hatch)


# --- A - B ---
A = {1, 2, 3, 4}
B = {3, 4, 5}
plt.figure()
v = venn2([A, B], set_labels=('', ''))
limpiar_etiquetas(v)
if v.get_patch_by_id('10'): aplicar_estilo(v.get_patch_by_id('10'), color='skyblue', hatch='///')
for region in ['01', '11']:
    if v.get_patch_by_id(region): aplicar_estilo(v.get_patch_by_id(region))

plt.title("A − B")
plt.savefig(f"{carpeta}/a-b.png", bbox_inches='tight', transparent=True)
plt.close()

# --- A ∩ B ---
A = {2, 3, 4}
B = {3, 4, 5}
plt.figure()
v = venn2([A, B], set_labels=('', ''))
limpiar_etiquetas(v)
if v.get_patch_by_id('11'): aplicar_estilo(v.get_patch_by_id('11'), color='mediumpurple', hatch='///')
for region in ['10', '01']:
    if v.get_patch_by_id(region): aplicar_estilo(v.get_patch_by_id(region))

plt.title("A ∩ B")
plt.savefig(f"{carpeta}/a-inter-b.png", bbox_inches='tight', transparent=True)
plt.close()

# --- A ∪ B ---
A = {1, 2}
B = {2, 3, 4}
plt.figure()
# Establecemos manualmente que todas las regiones tengan el mismo peso (por estética)
layout = DefaultLayoutAlgorithm(fixed_subset_sizes=(1, 1, 0.5))
#v = venn2([A, B], set_labels=('', ''))
v = venn2(subsets=(1, 1, 0.5), set_labels=('', ''), layout_algorithm=layout)
limpiar_etiquetas(v)
for region in ['10', '01', '11']:
    if v.get_patch_by_id(region):
        aplicar_estilo(v.get_patch_by_id(region), color='orange', hatch='')

plt.title("A ∪ B")
plt.savefig(f"{carpeta}/a-union-b.png", bbox_inches='tight', transparent=True)
plt.close()

# --- A △ B ---
A = {1, 2, 3}
B = {3, 4, 5}
plt.figure()
v = venn2([A, B], set_labels=('', ''))
limpiar_etiquetas(v)

for region in ['10', '01']:
    if v.get_patch_by_id(region):
        aplicar_estilo(v.get_patch_by_id(region), color='violet', hatch='///')
if v.get_patch_by_id('11'):
    aplicar_estilo(v.get_patch_by_id('11'))  # fondo blanco
plt.title("A △ B")
plt.savefig(f"{carpeta}/a-xor-b.png", bbox_inches='tight', transparent=True)
plt.close()

# --- B ⊆ A ---
A = {1, 2, 3, 4, 5}
B = {2, 4, 5}
plt.figure()
v = venn2([A, B], set_labels=('', ''))
limpiar_etiquetas(v)

# Pintar todo B como subconjunto dentro de A
if v.get_patch_by_id('11'):
    aplicar_estilo(v.get_patch_by_id('11'), color='lightgreen', hatch='///')
if v.get_patch_by_id('10'):
    aplicar_estilo(v.get_patch_by_id('10'), color='lightgreen')
if v.get_patch_by_id('01'):
    aplicar_estilo(v.get_patch_by_id('01'), color='white')  # No debería existir si B está contenido, pero por si acaso

plt.title("B ⊆ A")
plt.savefig(f"{carpeta}/b-subset-a.png", bbox_inches='tight', transparent=True)
plt.close()

# --- (A ∪ B)' ≡ A' ∩ B' ---
A = {1, 2, 3}
B = {3, 4, 5}
plt.figure()
ax = plt.gca()
ax.set_facecolor("white")

# Diagrama de Venn sin etiquetas
v = venn2([A, B], set_labels=('', ''))
#limpiar_etiquetas(v)
for label in v.set_labels:
    if label: label.set_text('')
for label in v.subset_labels:
    if label: label.set_text('')


# Zonas de A ∪ B en blanco con borde visible
for region in ['10', '01', '11']:
    patch = v.get_patch_by_id(region)
    if patch:
        patch.set_facecolor('white')
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
        patch.set_alpha(1.0)
        patch.set_zorder(3)  # Traer al frente

# Dibujamos el rectángulo que simula el universo con tramado
rect = Rectangle(
    (-2, -2), 5.0, 4.0,
    facecolor='lightgray',
    hatch='///',
    edgecolor='black',
    linewidth=1.0,
    zorder=0  # Enviamos al fondo
)
ax.add_patch(rect)

plt.title("(A ∪ B)' ≡ A' ∩ B'")
plt.savefig(f"{carpeta}/demorgan1.png", bbox_inches='tight', transparent=True)
plt.close()

# --- (A ∩ B)' ≡ A' ∪ B' ---
A = {1, 2, 3}
B = {3, 4, 5}
plt.figure()
ax = plt.gca()
ax.set_facecolor("white")

# Fondo con hatch para representar el universo 
rect = Rectangle(
    (-2, -2), 5.0, 4.0,
    facecolor='orange',
    edgecolor='black',
    linewidth=1.0,
    zorder=0  # Asegura que esté bien al fondo
)
ax.add_patch(rect)

# Diagrama de Venn
v = venn2([A, B], set_labels=('', ''))

# Etiquetas fuera
for label in v.set_labels + v.subset_labels:
    if label:
        label.set_text('')

# Intersección ('11') en blanco
patch = v.get_patch_by_id('11')
if patch:
    patch.set_facecolor('white')
    patch.set_edgecolor('black')
    patch.set_linewidth(1.5)
    patch.set_alpha(1.0)
    patch.set_zorder(5)

# Áreas 'solo A' y 'solo B' con color
for region in ['10', '01']:
    patch = v.get_patch_by_id(region)
    if patch:
        #patch.set_facecolor('orange')
        patch.set_facecolor('none')  # Deja pasar el fondo
        patch.set_edgecolor('black')
        patch.set_linewidth(1.5)
        patch.set_zorder(3)

plt.title("(A ∩ B)' ≡ A' ∪ B'")
plt.savefig("graficos/demorgan2.png", bbox_inches='tight', transparent=True)
plt.close()

# --- A ∩ B = ∅ (Disjuntos) ---
A = {1, 2}
B = {3, 4, 5}
plt.figure()

# Forzar tamaños iguales para A y B (regiones 10 y 01), y 0 para intersección
layout = DefaultLayoutAlgorithm(fixed_subset_sizes=(1, 1, 0))

# Generamos el diagrama manualmente
v = venn2(subsets=(1, 1, 0), set_labels=('', ''), layout_algorithm=layout)


# Limpiar etiquetas si usás esta función
limpiar_etiquetas(v)

# Colorear ambos círculos
for region in ['10', '01']:
    if v.get_patch_by_id(region):
        aplicar_estilo(v.get_patch_by_id(region), color='lightblue', hatch='')

# Asegurar que la intersección esté vacía y sin color
patch = v.get_patch_by_id('11')
if patch:
    patch.set_facecolor('white')  # no hay intersección
    patch.set_alpha(0)
    patch.set_edgecolor('none')

plt.title("A ∩ B = ∅ (Disjuntos)")
plt.savefig("graficos/disjuntos.png", bbox_inches='tight', transparent=True)
plt.close()


# --- A' (Complemento de A) ---
A = {1, 2, 3}
#U = {1, 2, 3, 4, 5}
plt.figure()
ax = plt.gca()
ax.set_facecolor('white')

# Venn para conjunto A (como primer conjunto, B vacío)
v = venn2([A, set()], set_labels=('', ''))

# Etiquetas fuera
for label in v.set_labels + v.subset_labels:
    if label:
        label.set_text('')

# Zona A completamente blanca
patch = v.get_patch_by_id('10')
if patch:
    patch.set_facecolor('white')  # Zona A
    patch.set_edgecolor('black')
    patch.set_linewidth(1.5)
    patch.set_alpha(1.0)
    patch.set_zorder(3)

# 2. Fondo tramado — después del diagrama, pero con zorder bajo
rect = Rectangle(
    (-2, -2), 5.0, 4.0,
    facecolor='lightgray',
    hatch='///',
    edgecolor='black',
    linewidth=1.0,
    zorder=0
)
ax.add_patch(rect)

plt.title("A' (Complemento de A)")
plt.savefig("graficos/complemento-a.png", bbox_inches='tight', transparent=True)
plt.close()

print("🎉 ¡Gráficos guardados correctamente en la carpeta 'graficos/'!")