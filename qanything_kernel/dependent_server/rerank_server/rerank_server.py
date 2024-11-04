from functools import wraps
import sys
import os
import time

# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)

# 将项目根目录添加到sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_script_path))))

sys.path.append(root_dir)
print(root_dir)

from sanic import Sanic
from sanic.response import json
# from qanything_kernel.dependent_server.rerank_server.rerank_onnx_backend import RerankOnnxBackend
from qanything_kernel.dependent_server.rerank_server.rerank_torch_backend import RerankTorchBackend
#from qanything_kernel.configs.model_config import LOCAL_RERANK_MODEL_PATH, LOCAL_RERANK_THREADS
# from qanything_kernel.utils.general_utils import get_time_async
import argparse
from qanything_kernel.utils.custom_log import debug_logger, embed_logger, rerank_logger

# 接收外部参数mode
parser = argparse.ArgumentParser()
# mode必须是local或online
parser.add_argument('--use_gpu', action="store_true", help='use gpu or not')
parser.add_argument('--workers', type=int, default=1, help='workers')
# 检查是否是local或online，不是则报错
args = parser.parse_args()
print("args:", args)

app = Sanic("rerank_server")


# @get_time_async
# @app.route("/rerank_onnx", methods=["POST"])
# async def rerank(request):
#     data = request.json
#     query = data.get('query')
#     passages = data.get('passages')

#     onnx_backend: RerankOnnxBackend = request.app.ctx.onnx_backend
#     # onnx_backend: RerankAsyncBackend = request.app.ctx.onnx_backend

#     # result_data = await onnx_backend.get_rerank_async(query, passages)
#     result_data = onnx_backend.get_rerank(query, passages)
#     # print("local rerank query:", query, flush=True)
#     # print("local rerank passages number:", len(passages), flush=True)

#     return json(result_data)

# 异步执行环境下的耗时统计装饰器
def get_time_async(func):
    @wraps(func)
    async def get_time_async_inner(*args, **kwargs):
        s_time = time.perf_counter()
        res = await func(*args, **kwargs)  # 注意这里使用 await 来调用异步函数
        e_time = time.perf_counter()
        if 'embed' in func.__name__:
            embed_logger.info('函数 {} 执行耗时: {:.2f} 秒'.format(func.__name__, e_time - s_time))
        elif 'rerank' in func.__name__:
            rerank_logger.info('函数 {} 执行耗时: {:.2f} 秒'.format(func.__name__, e_time - s_time))
        else:
            debug_logger.info('函数 {} 执行耗时: {:.2f} 毫秒'.format(func.__name__, (e_time - s_time) * 1000))
        return res

    return get_time_async_inner


@get_time_async
@app.route("/rerank_torch", methods=["POST"])
async def rerank_torch(request):
    data = request.json
    query = data.get('query')
    passages = data.get('passages')

    torch_backend: RerankTorchBackend = request.app.ctx.torch_backend
    result_data = torch_backend.get_rerank(query, passages)
    return json(result_data)


@app.listener('before_server_start')
async def setup_onnx_backend(app, loop):
    # app.ctx.onnx_backend = RerankAsyncBackend(model_path=LOCAL_RERANK_MODEL_PATH, use_cpu=not args.use_gpu,
    #                                           num_threads=LOCAL_RERANK_THREADS)
    # app.ctx.onnx_backend = RerankOnnxBackend(use_cpu=not args.use_gpu)
    app.ctx.torch_backend = RerankTorchBackend(use_cpu=not args.use_gpu)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, workers=args.workers)
