"""
This type stub file was generated by pyright.
"""

"""Group multiple small images into larger textures.

This module is used by :py:mod:`pyglet.resource` to efficiently pack small
images into larger textures.  :py:class:`~pyglet.image.atlas.TextureAtlas` maintains one texture;
:py:class:`TextureBin` manages a collection of atlases of a given size.

Example usage::

    # Load images from disk
    car_image = pyglet.image.load('car.png')
    boat_image = pyglet.image.load('boat.png')

    # Pack these images into one or more textures
    bin = TextureBin()
    car_texture = bin.add(car_image)
    boat_texture = bin.add(boat_image)

The result of :py:meth:`TextureBin.add` is a :py:class:`TextureRegion`
containing the image. Once added, an image cannot be removed from a bin (or an 
atlas); nor can a list of images be obtained from a given bin or atlas -- it is 
the application's responsibility to keep track of the regions returned by the
``add`` methods.

.. versionadded:: 1.1
"""
class AllocatorException(Exception):
    """The allocator does not have sufficient free space for the requested
    image size."""
    ...


class _Strip:
    __slots__ = ...
    def __init__(self, y, max_height) -> None:
        ...
    
    def add(self, width, height): # -> tuple[int, Unknown]:
        ...
    
    def compact(self): # -> None:
        ...
    


class Allocator:
    """Rectangular area allocation algorithm.

    Initialise with a given ``width`` and ``height``, then repeatedly
    call `alloc` to retrieve free regions of the area and protect that
    area from future allocations.

    `Allocator` uses a fairly simple strips-based algorithm.  It performs best
    when rectangles are allocated in decreasing height order.
    """
    __slots__ = ...
    def __init__(self, width, height) -> None:
        """Create an `Allocator` of the given size.

        :Parameters:
            `width` : int
                Width of the allocation region.
            `height` : int
                Height of the allocation region.

        """
        ...
    
    def alloc(self, width, height): # -> tuple[int, int]:
        """Get a free area in the allocator of the given size.

        After calling `alloc`, the requested area will no longer be used.
        If there is not enough room to fit the given area `AllocatorException`
        is raised.

        :Parameters:
            `width` : int
                Width of the area to allocate.
            `height` : int
                Height of the area to allocate.

        :rtype: int, int
        :return: The X and Y coordinates of the bottom-left corner of the
            allocated region.
        """
        ...
    
    def get_usage(self): # -> float:
        """Get the fraction of area already allocated.

        This method is useful for debugging and profiling only.

        :rtype: float
        """
        ...
    
    def get_fragmentation(self): # -> float:
        """Get the fraction of area that's unlikely to ever be used, based on
        current allocation behaviour.

        This method is useful for debugging and profiling only.

        :rtype: float
        """
        ...
    


class TextureAtlas:
    """Collection of images within a texture."""
    def __init__(self, width=..., height=...) -> None:
        """Create a texture atlas of the given size.

        :Parameters:
            `width` : int
                Width of the underlying texture.
            `height` : int
                Height of the underlying texture.

        """
        ...
    
    def add(self, img, border=...):
        """Add an image to the atlas.

        This method will fail if the given image cannot be transferred
        directly to a texture (for example, if it is another texture).
        :py:class:`~pyglet.image.ImageData` is the usual image type for this method.

        `AllocatorException` will be raised if there is no room in the atlas
        for the image.

        :Parameters:
            `img` : `~pyglet.image.AbstractImage`
                The image to add.
            `border` : int
                Leaves specified pixels of blank space around
                each image added to the Atlas.

        :rtype: :py:class:`~pyglet.image.TextureRegion`
        :return: The region of the atlas containing the newly added image.
        """
        ...
    


class TextureBin:
    """Collection of texture atlases.

    :py:class:`~pyglet.image.atlas.TextureBin` maintains a collection of texture atlases, and creates new
    ones as necessary to accommodate images added to the bin.
    """
    def __init__(self, texture_width=..., texture_height=...) -> None:
        """Create a texture bin for holding atlases of the given size.

        :Parameters:
            `texture_width` : int
                Width of texture atlases to create.
            `texture_height` : int
                Height of texture atlases to create.
            `border` : int
                Leaves specified pixels of blank space around
                each image added to the Atlases.

        """
        ...
    
    def add(self, img, border=...):
        """Add an image into this texture bin.

        This method calls `TextureAtlas.add` for the first atlas that has room
        for the image.

        `AllocatorException` is raised if the image exceeds the dimensions of
        ``texture_width`` and ``texture_height``.

        :Parameters:
            `img` : `~pyglet.image.AbstractImage`
                The image to add.
            `border` : int
                Leaves specified pixels of blank space around
                each image added to the Atlas.

        :rtype: :py:class:`~pyglet.image.TextureRegion`
        :return: The region of an atlas containing the newly added image.
        """
        ...
    


