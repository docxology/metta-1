import io
import logging
import os
import torch
import torch.distributed as dist

logger = logging.getLogger("dist_util")

def send_object(obj, dst_rank=0):
    """
    Send a Python object to the destination rank using torch.distributed.

    Args:
        obj: The Python object to send
        dst_rank: The destination rank (default: 0)
    """
    if not dist.is_initialized():
        logger.warning("Distributed training not initialized, skipping send")
        return

    # Serialize the object to a buffer
    buffer = io.BytesIO()
    torch.save(obj, buffer)
    buffer.seek(0)

    # Get the size of the serialized object
    size = torch.tensor(buffer.getbuffer().nbytes, dtype=torch.long)

    # Send the size
    dist.send(size, dst=dst_rank)

    # Send the serialized data
    data = torch.ByteTensor(list(buffer.getbuffer()))
    dist.send(data, dst=dst_rank)

    logger.debug(f"Sent object of size {size.item()} bytes to rank {dst_rank}")

def recv_object(src_rank=0):
    """
    Receive a Python object from the source rank using torch.distributed.

    Args:
        src_rank: The source rank (default: 0)

    Returns:
        The received Python object
    """
    if not dist.is_initialized():
        logger.warning("Distributed training not initialized, skipping receive")
        return None

    # Receive the size
    size = torch.tensor(0, dtype=torch.long)
    dist.recv(size, src=src_rank)

    # Receive the serialized data
    data = torch.ByteTensor(size.item())
    dist.recv(data, src=src_rank)

    # Deserialize the object
    buffer = io.BytesIO(data.numpy().tobytes())
    obj = torch.load(buffer)

    logger.debug(f"Received object of size {size.item()} bytes from rank {src_rank}")
    return obj

def broadcast_object(obj, src_rank=0):
    """
    Broadcast a Python object from the source rank to all processes.

    Args:
        obj: The Python object to broadcast (only needed on src_rank)
        src_rank: The source rank (default: 0)

    Returns:
        The broadcast Python object
    """
    if not dist.is_initialized():
        logger.warning("Distributed training not initialized, skipping broadcast")
        return obj

    rank = dist.get_rank()

    if rank == src_rank:
        # Serialize the object to a buffer
        buffer = io.BytesIO()
        torch.save(obj, buffer)
        buffer.seek(0)

        # Get the size of the serialized object
        size = torch.tensor(buffer.getbuffer().nbytes, dtype=torch.long)

        # Convert buffer to tensor
        data = torch.ByteTensor(list(buffer.getbuffer()))
    else:
        # Create empty tensors to receive data
        size = torch.tensor(0, dtype=torch.long)
        data = None  # Will be initialized after receiving size

    # Broadcast the size
    dist.broadcast(size, src=src_rank)

    # Initialize data tensor on non-source ranks
    if rank != src_rank:
        data = torch.ByteTensor(size.item())

    # Broadcast the data
    dist.broadcast(data, src=src_rank)

    # Deserialize on non-source ranks
    if rank != src_rank:
        buffer = io.BytesIO(data.numpy().tobytes())
        obj = torch.load(buffer)

    logger.debug(f"Broadcast object of size {size.item()} bytes from rank {src_rank}")
    return obj
