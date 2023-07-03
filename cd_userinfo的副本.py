{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# user_id:用户ID，order_dt:购买日期，order_products:购买产品数量,order_amount:购买金额\n",
    "# 数据时间：1997年1月~1998年6月用户行为数据，约6万条"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from datetime import datetime\n",
    "%matplotlib inline\n",
    "plt.style.use('ggplot')  #更改绘图风格，R语言绘图库的风格\n",
    "plt.rcParams['font.sans-serif'] = ['SimHei']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>user_id</th>\n",
       "      <th>order_dt</th>\n",
       "      <th>order_products</th>\n",
       "      <th>order_amount</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>19970101</td>\n",
       "      <td>1</td>\n",
       "      <td>11.77</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>19970112</td>\n",
       "      <td>1</td>\n",
       "      <td>12.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>19970112</td>\n",
       "      <td>5</td>\n",
       "      <td>77.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>19970102</td>\n",
       "      <td>2</td>\n",
       "      <td>20.76</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>3</td>\n",
       "      <td>19970330</td>\n",
       "      <td>2</td>\n",
       "      <td>20.76</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   user_id  order_dt  order_products  order_amount\n",
       "0        1  19970101               1         11.77\n",
       "1        2  19970112               1         12.00\n",
       "2        2  19970112               5         77.00\n",
       "3        3  19970102               2         20.76\n",
       "4        3  19970330               2         20.76"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 导入数据\n",
    "columns = ['user_id','order_dt','order_products','order_amount']\n",
    "df = pd.read_table('CDNOW_master.txt',names=columns,sep='\\s+')  #sep:'\\s+':匹配任意个空格\n",
    "df.head()\n",
    "#1.日期格式需要转换\n",
    "#2.存在同一个用户一天内购买多次行为"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>user_id</th>\n",
       "      <th>order_dt</th>\n",
       "      <th>order_products</th>\n",
       "      <th>order_amount</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>69659.000000</td>\n",
       "      <td>6.965900e+04</td>\n",
       "      <td>69659.000000</td>\n",
       "      <td>69659.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>mean</th>\n",
       "      <td>11470.854592</td>\n",
       "      <td>1.997228e+07</td>\n",
       "      <td>2.410040</td>\n",
       "      <td>35.893648</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>std</th>\n",
       "      <td>6819.904848</td>\n",
       "      <td>3.837735e+03</td>\n",
       "      <td>2.333924</td>\n",
       "      <td>36.281942</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>min</th>\n",
       "      <td>1.000000</td>\n",
       "      <td>1.997010e+07</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25%</th>\n",
       "      <td>5506.000000</td>\n",
       "      <td>1.997022e+07</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>14.490000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50%</th>\n",
       "      <td>11410.000000</td>\n",
       "      <td>1.997042e+07</td>\n",
       "      <td>2.000000</td>\n",
       "      <td>25.980000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>75%</th>\n",
       "      <td>17273.000000</td>\n",
       "      <td>1.997111e+07</td>\n",
       "      <td>3.000000</td>\n",
       "      <td>43.700000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>max</th>\n",
       "      <td>23570.000000</td>\n",
       "      <td>1.998063e+07</td>\n",
       "      <td>99.000000</td>\n",
       "      <td>1286.010000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "            user_id      order_dt  order_products  order_amount\n",
       "count  69659.000000  6.965900e+04    69659.000000  69659.000000\n",
       "mean   11470.854592  1.997228e+07        2.410040     35.893648\n",
       "std     6819.904848  3.837735e+03        2.333924     36.281942\n",
       "min        1.000000  1.997010e+07        1.000000      0.000000\n",
       "25%     5506.000000  1.997022e+07        1.000000     14.490000\n",
       "50%    11410.000000  1.997042e+07        2.000000     25.980000\n",
       "75%    17273.000000  1.997111e+07        3.000000     43.700000\n",
       "max    23570.000000  1.998063e+07       99.000000   1286.010000"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df.describe()\n",
    "#1.用户平均每笔订单购买2.4个商品，标准差2.3，稍微有点波动，属于正常。\n",
    "#然而75%分位数的时候，说明绝大多数订单的购买量都不多，围绕在2~3个产品左右；\n",
    "#2.购买金额，反映出大部分订单消费金额集中在中小额，30~45左右"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 69659 entries, 0 to 69658\n",
      "Data columns (total 4 columns):\n",
      " #   Column          Non-Null Count  Dtype  \n",
      "---  ------          --------------  -----  \n",
      " 0   user_id         69659 non-null  int64  \n",
      " 1   order_dt        69659 non-null  int64  \n",
      " 2   order_products  69659 non-null  int64  \n",
      " 3   order_amount    69659 non-null  float64\n",
      "dtypes: float64(1), int64(3)\n",
      "memory usage: 2.1 MB\n"
     ]
    }
   ],
   "source": [
    "df.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 数据预处理"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>user_id</th>\n",
       "      <th>order_dt</th>\n",
       "      <th>order_products</th>\n",
       "      <th>order_amount</th>\n",
       "      <th>order_date</th>\n",
       "      <th>month</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>19970101</td>\n",
       "      <td>1</td>\n",
       "      <td>11.77</td>\n",
       "      <td>1997-01-01</td>\n",
       "      <td>1997-01-01</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>19970112</td>\n",
       "      <td>1</td>\n",
       "      <td>12.00</td>\n",
       "      <td>1997-01-12</td>\n",
       "      <td>1997-01-01</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>19970112</td>\n",
       "      <td>5</td>\n",
       "      <td>77.00</td>\n",
       "      <td>1997-01-12</td>\n",
       "      <td>1997-01-01</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>19970102</td>\n",
       "      <td>2</td>\n",
       "      <td>20.76</td>\n",
       "      <td>1997-01-02</td>\n",
       "      <td>1997-01-01</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>3</td>\n",
       "      <td>19970330</td>\n",
       "      <td>2</td>\n",
       "      <td>20.76</td>\n",
       "      <td>1997-03-30</td>\n",
       "      <td>1997-03-01</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   user_id  order_dt  order_products  order_amount order_date      month\n",
       "0        1  19970101               1         11.77 1997-01-01 1997-01-01\n",
       "1        2  19970112               1         12.00 1997-01-12 1997-01-01\n",
       "2        2  19970112               5         77.00 1997-01-12 1997-01-01\n",
       "3        3  19970102               2         20.76 1997-01-02 1997-01-01\n",
       "4        3  19970330               2         20.76 1997-03-30 1997-03-01"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df['order_date'] = pd.to_datetime(df['order_dt'],format='%Y%m%d')\n",
    "#format参数：按照指定的格式去匹配要转换的数据列。\n",
    "#%Y:四位的年份1994   %m:两位月份05  %d:两位月份31  \n",
    "#%y：两位年份94  %h:两位小时09  %M：两位分钟15    %s:两位秒 \n",
    "#将order_date转化成精度为月份的数据列\n",
    "df['month'] = df['order_date'].astype('datetime64[M]')  #[M] :控制转换后的精度\n",
    "df.head()\n",
    "# df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0.5, 1.0, '每月的消费人数')"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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fr+GDh2qjIwM/fnPf1ZqaqruuecejRkzRnfffbdmzJihoUOHyu12SwqMsz322GMqLy/X8uXL1aJFC/l8PlVWVsoYo2+//bbGVSyXy1Vjnt/n8+ncc8/VhAkTav2Mc+fO1c6dO0/4fQAAAA1XWVmZBg0apNatW2v48OFKSkqS2+1WRUVFjQtpZWVl6tWr1zEj/cYY/e///q+WLl1a6+sfPnz4mLWqqip9/PHHGjhwoKRAF09MTIxeeeUVTZs2Tddcc40kafPmzcFu8T179igzM1MTJ07UsGHDJAW618eMGSMp0AEuBS4qVnvrrbeCr7V//34lJycrKytLf/3rXzV37ly98847evvttzV//vwaOevR3e6lpaV68skn9fLLL+uf//ynBgwYELzvhhtuUIsWLTRs2DA9/fTTuuOOOzRq1Cg1b95cb775pl5//XX95S9/0fz58yVJl112mV566SVlZGTo6quv1o033qipU6fqww8/1Ouvv66LL774uP9OAE4dhSKggQmXZOP7kpOTNWXKFPXv3z84sjVr1iwtXrxYzZo1q/U5x2tLrladsBzN5XKprKxMQ4YM0cGDB+VyuTR79uxgZ9XRo21NmjQ5pnBmjNGCBQs0evRoDRkyRNnZ2SotLQ12Ov3mN7+pUUi75JJL9J///EfDhw/XhRdeqIyMDLVt21Z//OMfNXnyZI0YMUJvvfWW8vPz1axZMxUVFQVj9/v9ateune6//37t3r271s/Yrl07DRo0SNZaVVVVnbR4BgAAGpbExEQ999xz6tGjh/75z3/q+uuv1/Tp03XttdeqY8eOevLJJ+VyufTOO+/o448/rvU1TtYN/n1H5zvVZs6cKZfLpZ/97GfBNZ/Pp8TERElSixYtdO2112r48OG699579cILL8jlcqlr165atGjRMa/XvHnzGnnJ3r17tXHjRvXu3Vs5OTmqrKxU7969gx1FvXv3rvH8RYsWaevWrbruuuvk8Xh09dVXa9CgQYqJiQnmgPHx8aqqqtKgQYOUmZmpl156Seeff76uv/56vf/++1q0aJHeffddDR48WJdeeqmuv/56SYGi1X/9139p/vz5GjBggN5///1avycATg//RwI0MOGSbFSrLohceOGFuv/++1VcXBz85f/yyy/roYceUnJysioqKmStrVG4OXz4sBo3blyjC+ho99577zFrxphg0pKWliZJ+ve//63nnntOY8aM0ejRo4P7Afl8vhqfbefOnbrmmmv0wgsv6N133w12/hQWFuq8886TJGVkZNR4v9zcXN1yyy1yuVy69957tXDhQq1cuVJPPvmkZs2aFRxh+/bbb+X1eoPFvOzsbI0ePVqNGjVSkyZNTpi8lJeX6/7779ddd92lu++++7iPAwAADVPfvn0lfZcPSIFu56FDh6p///768Y9/rMOHDwc7lq21wdGvysrKOolh2LBhuvnmm3XTTTfp2Wef1bnnnqvKyspg7mWM0aRJk9SuXbtg3lOdnxzv4t3R+cs999yjESNG6NFHHw3uR9myZcsaexSVlpZqzpw5uvbaa5WcnKzu3bvr8ccf18iRIxUXF6eZM2dKCuR4qampx3RcjxkzRsYY+Xw+lZSU6JVXXtGoUaN0xx136IorrlD//v0lfdd1/vDDDwf3RqqtEx3A6aFQBDRA4ZBsVBs9evQxx5uOHDky+PcVK1bogQcekCSNHz8+mBD4fD653e7gZoTGGMXExAQLT9V8Pp9cLlfwl7+1VjExMUpKSgomL88995wKCgo0YsQIPf3008Hvh8/nq9Ed1Lp1a40ZM0Y///nPdeedd+rZZ59VTk6OiouLj7u30X/+8x81adJEM2bM0Msvv6zu3bvrxhtv1Ouvv67t27crNzdXUuDfqnXr1sHn9enTRxs2bFB2drb+/ve/n/B73bJlS91zzz0nfAwAAGi4Bg8erNWrVwf3JJw5c6aqqqpkjNFtt90mKTASb63VtGnT9MADD+gPf/iDpMCR9e+++65mz55d62sfvRfl0X784x8Hc6GSkhKlpqYGD+549tln9ec//1llZWXHXOQbOXJkjYNBFi9efMy2BN83a9YszZw5U59++mkwbxo0aFAw/uo9iqy1uvDCCzVhwoTg+44aNUqlpaXy+/3BeK218vv9wQJVVVWVqqqqlJSUJCmwPcFTTz2lnJwcNW7cWO3bt9fHH3+sm2++WS+99FIwrrKyMrVt2/aEsQP44Si7Ag3Q4MGD5fV69eCDD2rq1Klq3ry5OnTooG3btum2225T8+bNdd999+m1115TSkqKnnzyyeBzq5ON5s2b1/p1omQjOTlZycnJ2rVrl1JTU9WzZ89gsiGp1mTDGKOHH35Y1toTfvn9/uAx8hs2bFBcXFyNr+pCzfXXX3/MfTfeeGPw/fx+v4qKioLdRFVVVZKkN998U3fddZcWL14cfPz3C0WSdPvtt2vFihXBEbrNmzerbdu2x+34ueaaa/TGG2/o4MGDevjhh/XLX/5SLVq0UMeOHfXwww+rsrJSu3fv1qZNm2ps1F1ty5Ytmj9/vq666ipdddVVSktL06JFi4K3U1JS9N5779X63gAAIDx8+umnOnjwoO666y698MIL2r9/vzp16qR77rlH33zzjfbv3697771XTz31lAoLC4NFIinQvfzEE09o//79tX7VdgiJJH3yyScqKipSUVGRWrVqFVy/77779Prrr6ugoEBlZWXHHJrx73//W/369QsWi6r//v2v6lPQpEBHekZGhmbMmKEuXbpo165d2rRpk6ZOnaoFCxaooKBAs2fP1pYtW/TRRx9p/PjxNd7z1ltvVdOmTZWamqrU1FRNnTpVkydPDt5OTU2tsSl1ZWWl/vznP6tTp066/PLLtWTJEq1fv15bt27VnDlzZK1VeXm5ysrKdO65557+PxyAWlEoAhqgcEo2Dh06FCzanMjRI2NxcXFq3bp1MBHZvn17MK64uDhNnz49eN+rr75aY2+mqqoqbdu2LbjvUWVlpXbs2KGnn35aGRkZ+uabb/TPf/4z2KlU/Z433HCDUlNT1bx5c1122WW69dZb1bx5cw0ZMkQ7d+4MFtLOOussNW3aNFhImj59us4991y1a9dO8fHx6tGjh1JSUvTCCy/ooYce0qBBg/TRRx9pyZIl6tWrV62f/auvvtKjjz6qRx99VG+++aY2b94cvP3WW28Fu8EAAEB4O3DgQLBw8cEHH2jlypXBjZgPHz6sJk2aHPOc7Oxs9ejRo85iGDBggEaOHKmioiIVFxcfk/u988476tevXzD/+Pzzz4MXC4/+OvrwkoEDB2rChAnBbnYp0BV0++2364MPPqjx+tUX8Y723nvvafLkyVq7dq2Kior061//Wo888oiKior0xRdfaPTo0cFT16TAGNmqVauUkpKimTNn6pJLLlHfvn3Vp08f3XDDDSovL9e8efPUt2/f4Oc43gmzAH44Rs+ABuzAgQPBgsUHH3ygO+64Q/Pnz1dmZqYOHz4cnC8/WnZ2dnCjv7pwsmRj165duummm37Qa9ZWGKnu6DnRfZL0i1/8QosWLVKPHj1UWVmpWbNmqbS0VI0aNdKcOXN0wQUX6LzzztOsWbMkfXfC2zvvvHPM627YsEG9evXS7Nmz1adPnxoFqWp33nmnbr/9dnXq1Elvv/22unXrpmHDhmnIkCGSpFtuuUVjx47VgQMHaj3ZzOv1asiQIbrwwgslBY5xXblyZfDfNT8/n5l6AAAixNdff62bbrqpRkfzkiVLJAVGyGJjY/Xaa68FiyJffPGFdu/eHdx7p65MnTpVkjRv3jw1bdo0uL5371698847WrFihaRAsadPnz7H3cz6+44+9v61115Tbm6ubr/9do0fP179+/fXkCFDVFlZWWun9u7du3XDDTdo8eLFNdaff/557du3Lzh2JgVyvxkzZujnP/+5fvOb3ygzM1MTJkxQRUWFJCkrK0t33323JkyYoAceeEDPPPNM8JRbAGeOQhHQgDX0ZOPAgQNau3ZtcE+lU1VdDDp6Lr36F78xpsbM+vdPPnv99dfVvn17jRs3Tp06dVJWVpZatWqlrVu3Bh9z9dVXy+PxSNJxTxH74osv9POf/1z33ntv8HSyCRMmaOTIkcckN2vWrFFsbKx++9vfKiMjQwsWLNBbb70lSbryyitVWlqqzp071+jEqvbGG29o27Zt2rlzp6RAYSgnJ0dZWVnBz1dWVqacnJxgzAAAIDxV52lHO3TokLZt26abbrpJ06ZNCx664ff7NXbsWN1xxx3H5Cs+n0/r16/XgQMHVFhYeMzov8/n0+DBg4MXm8rLy2vdkHrNmjU1RsjuuecetW7dWp07d5ZUe/dPYWGhtmzZouLi4mMu4PXp00cTJ07UnXfeqZkzZ2r69Ony+/3auHGjJk2apL59+2r27Nm6+uqrg7GVlZXJ7/fr8ccfV58+fZSdnR3clmD9+vX64IMPtGLFCpWUlKiqqqpG15W1VqNGjVJSUpJycnJ0xx13qKSkRM8//7z69eunQYMG6T//+Y9uvPFG/etf/1L37t2P/48D4NRZAGElNzfXLl++3LZr184uWrTIlpSUWGutraqqspdffrl95JFHjnlOZWWlXb16tZ09e7Y1xth9+/bVuL9Tp042Li7OJiQk2ISEBCvJLl++/JjXeeCBB+y9994bvP3b3/7WZmZm/uDPsHnzZiupxte5555rrbX2xhtvPOa+kSNHBp97991326FDh1q/329HjRplO3fubA8fPnzMeyxbtswmJibaqqqqGuu7d++29913n/V6vXbKlCnB9c8++8xedNFFtmvXrvbzzz+vNe63337bpqSk2IEDB9qLLrrIlpWV2Weffda2adPGpqam2nffffeY5+zbty/4b2Sttf/3f/9nhw4dGrxdVVVlCwsLrd/vP8XvHgAACCerV6+2brfb3nXXXTXykhkzZthWrVrZ/Pz8Wp/XpUsXm5KSYq+77rpj7rvkkkvswoULg7cHDx5sV61aZa0N5BbDhg2z7du3tx06dLBffvmltdba0tJSO2nSJPvkk08Gnzd16lTbr1+/Gq9dUlJizznnHNunTx+bk5NjrbXW5/PZTp06WUk2JSXF3njjjXbt2rU1nrdz5077q1/9yjZq1MhmZ2cH1++9914bHx9vmzRpYps2bXrcr8aNG9uYmBibl5dX43P9+9//ttZaO378eDtq1Cjbvn17+7vf/a5G7vS73/3OTp06tdbvI4AfjkIREGYaSrLxxRdf2Pj4eLtkyZIf/BnWr19vW7duHby9c+fO4O1f/OIXdvr06cH7Zs6caf/f//t/1lpr33zzTXvBBRfY/fv3W2utraiosD/+8Y/tunXrgo/3+Xz24osvti6Xy95zzz3B9a1bt9oePXrY5ORkO3r0aLt79+5j4iovL7ePPfaYjYuLCxbKCgsL7fvvv2+vvvpq27NnT/vFF19Ya639xz/+YQcMGGD79Olj9+/fbz/55BObmJhox4wZY8vLy6211vbu3dv27NnT9uvXL/h18cUX2xYtWtRY69u3r+3cubP95JNPfvD3EgAAhK/i4uLj3ldRUXHar7t27Vq7Z8+e035+aWnpMWvr1q2zGzZssJWVlSd8bkFBwWm/76k4Xq4LoO4Ya486GxFAWCspKakx3320ysrKkx59ejzr1q1Tenq6WrRoUWN9xYoVIW/xPZURrY0bN8rr9crr9dZYnzNnjvr06XPcDb2rbd68We3bt5cUaBe/5557dMMNN2jo0KHBxzz33HNq1KiR7rrrruCo2qpVq7R69Wrdfvvtp/PRAAAAAMBxFIoAAAAAAAAgSeKoHQAAAAAAAEiiUAQAAAAAAIAjaj83ugHZu3ev0yEAAI7weDzKyclxOgxEmO/vf4aGgRwMABoOcjDUtRPlX3QUAQAAAAAAQBKFIgAAAAAAABxBoQgAAAAAAACSKBQBAAAAAADgCApFAAAAAAAAkEShCAAAAAAAAEfEOh0AAAAApPz8fE2aNEnPPPOMpk6dqt27d6tbt24aPny4JNX5GgAAQG3oKAIAAGgA3nzzTVVUVCg7O1t+v18TJ07UgQMHtG/fvjpfAwAAOB46igAAABy2fv16JSQkKDU1VRs2bFCfPn0kSV26dNGmTZu0ffv2Ol07++yzj4khKytLWVlZkqTJkyfL4/HU++cGAJya2NhYfi4jZCgUAQAAOMjn8+mDDz7QAw88oGeffVbl5eVyu92SpOTkZG3fvr3O12qTmZmpzMzM4O2cnJx6+8wAgB/G4/Hwcxl1qkWLFse9j9EzAAAAB82aNUuDBw9W48aNJUmJiYmqqKiQJJWVlcnv99f5GgAAwPFQKAIAAHDQunXrNGfOHE2YMEE7duzQypUrtWnTJknSzp071axZM7Vt27ZO1wAAAI6H0TMAAAAHPf7448G/T5gwQQ8++KDGjx+vvLw8rVmzRhMnTpSkOl8DAACojbHWWqeDOJG9e/c6HQIA4Ajm41EfTjQjH62Kioq0du1adezYUampqfWydjLkYADQcJCDoa6dKP+iUNQA2JwD8v99msw5reW6eoTT4QDAcZGkoD5QKGqYIj0Hs5UVsos/k12cJdc1I2Q6X+p0SABwXORgqGsnyr8YPXOQ9ftl530s++FMqbxMdt9uiUIRAABAvbElxbLzP5HN+qdUmB9YW7+KQhEAAEdQKHKI3b9b/hkvSVu/lDpdIiU2ktavlrVWxhinwwMAAIgoNv+Q7Gf/Jzv/E6m0ROp0iVw//oX8f5sqm8dVegAAqlEoCjFbVSX76f/K/vN/pPgEmdvukelzhey//yG7colUUiw1TnY6TAAAgIhgv90rO2eW7JLPpKoqme79ZK4aJtPq/MAD0r1S7kFngwQAoAGhUBRCdte2QBfRrq+lbn3kGvFfMk3TAne6PbKSlHeQQhEAAMAZsju/lp39QeBCXEyMTN8rZYb8XKZZzT0ZjNsr+812h6IEAKDhoVAUArayUvajd2XnfCA1biLXfz0sc2nfmg9yewN/5uZI57YJfZAAAABhzlorbV4n/ycfSBtXS42SZK66VubKq7+7OPd9bo9UmC9bWSETFx/agAEAaIAoFNUz+/WmQBfRvm9k+lwuc/1omcZNjn3gkUKRPXRQ7FAEAABw6qzfL63Jln/2B9L2LVJKqsywW2V+dJVMUuMTPzntyMW6vBypGSfwAQBAoaie2PIy2f99U3buR1Jauly/HS9z8QlO00hJlWJiA6NnAAAAOCnrq5TNni87+wNp/x7J21zm5l/L9L3ilLuDTPX4/yEKRQAASBSK6oX98gv5Z06Rcg7IDPyJzPBbZBKTTvgc43JJaemB0TMAAAAcly0rlV34qeyns6T8XKllG5k7x8l06ysTE/PDXiydrm4AAI5GoagO2ZIi2fffkF34qdSshVzjJsm063zqL+D2yNJRBAAAUCt7uFB27keBju2SIqn9xXLdOkbqdImMOc0yT5on8OchLtYBACBRKKozdk22/G9NlQryZYYMk7n6Rpn4hB/0Gsbtlf1qYz1FCAAAEJ5s7rey//6H7MI5UkWF1LW3XFcNkzm/wxm/tomLl5o0lQ5xsQ4AAIlC0Rmzhwtk/+evsssXSue0luvu38ucd+HpvZjbK+XlyPqrZFw/sG0aAAAgwtg9O2Vnfyi7fIEkyfQaKHPVMJmzW9btG7m9shSKAACQRKHotFlrZZctkH3nVam0ROaaETJXDZeJjTv9F03zSH6/VJAf2K8IAAAgCtmtXwZOMPtimRSfIHP5UJlB18gcOSW2zrk9gc2wAQAAhaLTYfNy5f/by9La5VKbdnLd+luZc1qd8euadO+RUzcOUigCAABRxVorrV8p/yfvS19tlBo3kfnZjTJXDJVJTqnX9zZur+zGL2StPf29jgAAiBAUin4Aa23ghI33p0tVPplf3i5z5U/rbkzsyGaK9tDBOpm5BwAACBf+l5+W1iyV3B6Z60fLXDZYJiExNG/u9kjlpVJpsZSUHJr3BACggaJQdIrst/sCR95vXhc4YeOW38g0O7tu36S6nZpTNwAAQBSx+3dLa5YGxsuG3SoTG9oU1biP6uqmUAQAiHIUik7C+qtkP/tIdtabUkyszMi7A1e46qEt2SQ1lholceoGAACIKjZ7vmRcMoN/HvIikaTvLtbl5kjntgn9+wMA0ICc9DdxSUmJXnzxRfn9fiUkJGjs2LEaM2aMzjrrLEnSqFGj1KpVK7333ntavXq1zj//fI0ePVqSTnmtobJ7d8k/4yVp22Ypo4dcN/1Kxu2p3zdN88jSUQQAAKKEtVZ26TzpogyZVIf2aDyS39m8g2KHIgBAtDtpoWjhwoX66U9/qoyMDL366quaNWuW+vXrp5tvvjn4mG3btmnTpk2aNGmS3n//fa1du1bJycmntJaRkVGvH/B0WJ9Pdvb7sv96T0psJDP6fpmeA0KzuaHbS0cRAACIHl9vknIOyPzsRudiSEmTYmLJwQAA0CkUioYMGRL8e2FhodLT07Vq1Spt2LBBrVq10p133qmNGzeqV69eMsaoS5cuWrNmjZKSkk5p7fuFoqysLGVlZUmSJk+eLI+nnjt4vse3Z6cK/vSYfDu2KqF/plJuv1euVHfI3r+wxbkq2/V1yD83AJyK2NhYfj4BqFM2e54UHy/TrbdjMRiXS0p1s08kAAD6AXsUbdmyRcXFxcrIyNDll1+utLQ0TZkyRatXr1ZZWVlwFFRI2uYAACAASURBVC05OVn5+flyuVyntPZ9mZmZyszMDN7OyQntL+yqV56Tvt0v192/l69rLx3y+aUQxuBPaiJbmK+De/fIxCeE7H0B4FR4PJ6Q/1xG5GvRooXTIcAh1lcpu3yRTNfeMolJzgaT7pWlowgAALlO5UFFRUWaNm2afvWrX6l169ZKS0uTJLVt21b79u1TYmKiKioqJEllZWWy1p7yWkNiiwqljasDm1V37eVMEJx8BgAAosX6VVLxYZneA52ORMbtJf8CAECnUCjy+Xx6/vnnNWLECHm9Xr300kvasWOH/H6/li9frtatW6tt27batGmTJGnnzp3yer2nvNaQ2FWfS1VVMj0vcyyG4GbZeSQqAAAgstml86QmTaWLujodipTmkfJzZf1VTkcCAICjTloomjt3rrZv364PP/xQEyZMUMuWLTVlyhSNGzdO7dq1U0ZGhjp06KAdO3Zo+vTpmjVrlvr373/Kaw2JXbZAan6O1LKtc0Ec6Sii9RkAAEQyW1Is+8UymR6XycSe8m4I9cftlaqqpIJjt0YAACCanPS38uDBgzV48OAaa9ddd12N2y6XS4899phWrVqln/zkJ2rWrJkknfJaQ2DzD0lb1sv89PrQnG52PKnpkjFSLoUiAAAQueyqJZKvskGMnUmBrm4rBU4+S0t3OhwAABxTZ5dv4uPj1bt379NaawjsysWStTI9Bjgah4mLk1JSGT0DAAARzS6dJzVrIZ13odOhBAS7unNkznc4FgAAHHRKm1lHA7tsgdSyjczZ5zodiuTm1A0AABC57KGDgU7u3gOd7eQ+WvBAEXIwAEB0o1AkyR7cL23b7Hg3UVCahyQFAABELLtsQaCTu9ePnA4lyCQ1lhIb0dUNAIh6FIok2RWLJEmmR8PYXLv6eFZrrdOhAAAA1Dm7dJ50fgeZZmc7HUpNbq8s+0QCAKIchSJJdtnCQLLiOcvpUALSPVJFuVR82OlIAAAA6pTdvV3as7PBbGJdg5uubgAAor5QZPd9I+3eLtPjMqdDCTJp1TPytD4DAIDIYpfOk2JiZLo3jE7uoxm3l9EzAEDUo1C0bKFkXA0rWWEzRQAAEIGsv0o2e4HU+VKZ5BSnwzmW2ysdLpCtKHc6EgAAHBPVhSJrrezyhVL7zjJN05wO5ztujyRx8hkAAIgsm9dL+blyNcSxMylwoIgk5eU6GwcAAA6K6kKRdm2TDuxpUGNnkqQmTaXYWEbPAABARLFL50mNkqSMHk6HUiuTTlc3AABRXSiyyxcEZuQv7et0KDUYlytwRYskBQAARAhbXi67aolMt74y8QlOh1O7NLq6AQCI2kKR9ftlly+SOl4i07iJ0+Ecy+2VZTNFAAAQIezaZVJZacM87axa9egZXd0AgCgWtYUibdskHToo03OA05HUynA8KwAAiCB26bxAIaZdZ6dDOS4TFyc1TSMHAwBEtagtFNllC6W4eJmuPZ0OpXZur5R3SLaqyulIAAAAzog9XCBtWCXTc0BgxL4hS/PI0lEEAIhiDfw3df2wVVWyKxZJGd1lEpOcDqd2bo9k/VLBIacjAQAAOCN2xSKpqqphj51Vc3vpKAIARLWoLBRp8zrpcIFcDXTsTJKMm1M3AABAZLBL50nnnidz7nlOh3JS1eP/1lqnQwEAwBFRWSiyyxdKiY2kzpc6HcrxpQUKRTaXQhEAAAhf9tu90rbN4dFNJAU6iirKpZIipyMBAMARUVcospWVgaNZL+ndcI9mlQKjZ5LEyWcAACCM2aXzJWNkejTcTu6jBbu6uVgHAIhSUVco0sbVUklxg09WTKMkKakxo2cAAESBoqIirV27VoWFhU6HUqestbLZ86T2FwdGusIBF+sAAFEu1ukAQs0uWyglN5Eu6uJ0KCfHqRsAAES8oqIiTZ48Wd26ddOMGTM0fvx4PfTQQzrrrLMkSaNGjVKrVq303nvvafXq1Tr//PM1evRoSTqjtZDYvkX6dp/MT64L3XueqSMdRfbQQRmHQwEAwAlRVSiy5eWyX2TL9BooExsGH51TNwAAiHi7du3SLbfconbt2qmoqEhz585Vv379dPPNNwcfs23bNm3atEmTJk3S+++/r7Vr1yo5Ofm01zIyMkLy2ezSeVJcvMwlfULyfnWiSVMpNpbRMwBA1AqDakndsWuXS+VlMj0vczqUU2LcHtltm50OAwAA1KOOHTtKkjZu3Kivv/5avXr10qpVq7Rhwwa1atVKd955pzZu3KhevXrJGKMuXbpozZo1SkpKOu212gpFWVlZysrKkiRNnjxZHs+ZjYpZn08HVy5WQs/LlNqq9Rm9VqjlpDdTXMlhNT3D7wEA1JXY2Ngz/rkMnKroKhQtWyA1dUsXdnQ6lFPj9krFh2XLy2QSEp2OBgAA1BNrrZYsWaLGjRurTZs2euyxx5SWlqYpU6Zo9erVKisrC46iJScnKz8/Xy6X67TXapOZmanMzMzg7ZycMxt/t2uXyxbmq/KSPmf8WqFWlZquqn27VRlmcQOIXB6PJ+x+lqJha9GixXHvi5rNrG1JsbR+hUyP/jKuGKfDOTXVp26wTxEAABHNGKPRo0erVatWysvLU1pamiSpbdu22rdvnxITE1VRUSFJKisrk7X2jNZCwS6dF9gXstMlIXm/umTSPORfAICoFT2FojVLJZ9Ppkd4jJ1J+u50kDxm5AEAiFSzZs3S/PnzJUklJSV69dVXtWPHDvn9fi1fvlytW7dW27ZttWnTJknSzp075fV6z2itvtnSEtk12TLdL5OJjav396tzbq+UnytbVeV0JAAAhFz0FIqWLZA8Z0lt2jkdyqmrPnWDzRQBAIhYmZmZWrBggcaPHy+/36/HH39cU6ZM0bhx49SuXTtlZGSoQ4cO2rFjh6ZPn65Zs2apf//+Z7RW3+zqz6XKCpneA+v9vepFukfy+6WCQ05HAgBAyBkbqv7j07R3794zfg17uED+B26VGTJMrmG31EFUoWF9Pvl/PVxm6PVyXTPC6XAAgPl41IsTzcjjOxUVFVq1apXatGkT3HPoTNZO5kxysKrnH5NyDsg18RUZE36HzNt1K+X/78fleuiPMhdc5HQ4AEAOhjp3ovwrKjaztisXS35/2Jx2Vs3ExkpN0xg9AwAAio+PV+/evetsrb7Y/Fxp01qZodeHZZFI0ndd3YcOyohCEQAgukTF6JldvlA6u6V0znlOh/LDub2ybKYIAADChF22QLJWptePnA7l9AX3iSQHAwBEn4gvFNlDOdJXG2V6XhaWV7VMmkdijyIAABAm7NJ5Upt2Ms3PcTqU02YaJUmNGpODAQCiUuQXilYsClzV6jHA6VBOT7pXyssJ2VG2AAAAp8vu2Sl9sz18N7E+mtsje4hCEQAg+kR+oWj5Qqn1BTJnhelGmW6vVFkhFRU6HQkAAMAJ2ex5kssl0yO89oWsldvL6BkAICpFdKHIfrtX2vFVWCcrJu3IjDz7FAEAgAbM+v2y2fOlTt1kmjR1OpwzZtweiY4iAEAUiuxC0fJFkiTTo7/DkZyB9MCpGyQqAACgQftqg3QoJzLGziQpzSMVHZYtL3c6EgAAQirCC0ULpQs6yhw54jQsHekoYkYeAAA0ZHbpPCmhkUyXXk6HUjeqL9blkYMBAKJLxBaK7J6d0p6dMj3Dd+xMktSkqRQbx+gZAABosGxlhezKxTLd+sgkJDgdTp0IXmjkYh0AIMpEbqFo2ULJuGQu7ed0KGfEGBPYTJEkBQAANFRrl0ulJZEzdiYd1dXNxToAQHSJyEKRtVZ2+QLpogyZlFSnwzlzHM8KAAAaMP/SeVJTt9ThYqdDqTtp6ZIxXKwDAESdiCwUacdW6eB+mZ4DnI6kThi3l9EzAADQINmiQmndSpleA2RcMU6HU2dMbJyUkkahCAAQdSKyUGSXL5BiYmUu6e10KHXD7ZUKDsn6fE5HAgAAUINdsViq8sn0Guh0KHXP7WH0DAAQdSKuUGT9ftnli6TO3WSSkp0Op264PZK1UsEhpyMBAACowWbPk1q0klq2cTqUOkdXNwAgGkVcoUhbN0r5uREzdiYddepGLq3PAACg4bAH90tbv5TpPTBwAEekcXukvIOy1jodCQAAIRNxhSK7bIEUnyDTpafTodQdd/WpGxSKAABAw2Gz50uSTM8fORxJPXF7pYoKqeiw05EAABAyEVUosj6f7MolMl16yiQkOh1O3TlyPKvyaH0GAAANg7U2MHbWrrNMutfpcOqFOXKxjg2tAQDRJKIKRdq0VioqlOl5mdOR1CmT2Ehq3IQkBQAANBw7t0r798j0Huh0JPWnevw/jxwMABA9IqpQZJctkBo1ljpd6nQodS+NUzcAAEDDYZfOk2JjZS7t63Qo9edIocjmkoMBAKJHxBSKbGWF7JqlMt16y8TFOR1O3Uv30lEEAAAaBFtVFbhAl9Ezck6ZrU2TplJsHB1FAICoEjGFIq1fJZWWyPSInNPOjmbSPBSKAABAw/DlGulwgVyRPHYmBU5yc3skuroBAFEkYgpFdtmCwFWfDhlOh1I/3F6ppFi2rMTpSAAAQJSzS+dJSclS5wgc9/8+t5eTZwEAUSUiCkW2rFR27TKZS/vJxMQ4HU79CJ66wRUtAADgHFtWKrt6qUz3/pE57v89ga5u8i8AQPSIjELRF8ukigqZHpF12tnRTPWpG1zRAgAADrJrlkoV5ZF92tnR0r1S/iHZqiqnIwEAICQio1C0fKGU5pEuuMjpUOpP9akbXNECAAAOskvnSenNpPM7OB1KaKR5JOuX8g85HQkAACER9oUiW1wkrV8l06O/jCvsP87xpbol46KjCAAAOMYW5Ekbv5DpNTCy866j0NUNAIg2Yf8b3q5aIlX5InrsTFJg76VUNzPyAADAMXb5Asn6ZXr/yOlQQie9uqubQhEAIDqEf6Fo+UKp2dlS6wucDqX+uT0kKQAAwDF26Xyp9QUyZ7d0OpTQSeNAEQBAdAnrQpEtyJM2rZPpcZmMMU6HU++M20vbMwAAcITd9420c2t0dRNJMomNpKRkcjAAQNQI70LRysWB9uceA5wOJTTcHikvV9bvdzoSAAAQZezSeZLLJdMzSvKuo7k9snl0FAEAokN4F4qWL5TOaS1zTiunQwkNt1fyVUpFBU5HAgAAooj1+2Wz50sdu8qkpDkdTui5vVIuHUUAgOgQtoUim3tQ2vplxG9ifTTjZkYeAAA4YOuXUu63Mr0GOh2JIxj/BwBEk/AtFK1YKEnR1f7M8awAAMABNnuelJAoc0lvp0NxhtsjlRTJlpU6HQkAAPUufAtFyxZIbdrJeJs7HUropHE8KwAACC1bWSm7YpHMJb1lEhKdDscZ1Rfr2KcIABAFwrJQZPfvlnZti6qxM0lSchMpPp7RMwAAEDrrVkglxVE7diZJJu3I+D/7FAEAokB4FoqWL5KMkene3+lQQsoYI7m9dBQBAICQ8WfPk1JSpYu6OB2Kc9KPdHXTUQQAiAJhVyiy1gbGzi7sJJOW7nQ4oZfmoaMIAACEhC0uktYul+k5QCYmxulwnNPULRkX+0QCAKJC2BWKtHuHtH93dG1ifZTAqRsUigAAQP2zKxdLPp9M74FOh+IoExsrNU0jBwMARIWwKxTZZQskl0umW1+nQ3GG2yMV5sn6Kp2OBAAARDibPU9qfq7U6nynQ3FeOuP/AIDoEFaFImut7PKFUseuMk1SnA7HGW6vZK2Ul+t0JAAAIILZ3G+lLRtkeg8M7JMY5Uyah9EzAEBUCKtCkbZtlnK/lekRnWNn0pHRM4nWZwAAUK9s9nxJitpx/2McGf+31jodCQAA9SqsCkV2+UIpNk6may+nQ3GOO3A8K63PAACgPtml86QLOsp4mzsdSsPg9kq+SulwgdORAABQr8KmUGT9VbIrFkkXXyqT1NjpcJyTVt1RRKEIAADUo33fRP0m1kczRy7WKY+ubgBAZAubQpG2bJAK8uSK8vZnk5AgJacwegYAQAQpKirS2rVrVVhY6HQo34mJlenez+koGo7q8f9cLtYBACJbrNMBnCq7bIGU0Ei6uIfToTjP7ZHlahYAABGhqKhIkydPVrdu3TRjxgyNHz9eb731lnbv3q1u3bpp+PDhkqSpU6fW6dpJXdxdpnGTuv/A4eqo8X+29gYARLKTFopKSkr04osvyu/3KyEhQWPHjtWrr74a0kTF+iplV30u07VnoKMm2rm90sH9TkcBAADqwK5du3TLLbeoXbt2Kioq0vr16+X3+zVx4kS9/PLL2rdvn3bt2lWna2efffZJ43IxdlZTcooUF8/oGQAg4p20ULRw4UL99Kc/VUZGhl599VUtXrw45ImKNq6Rig9H9WlnRzNpHtnN65wOAwAA1IGOHTtKkjZu3Kivv/5aRUVF6tOnjySpS5cu2rRpk7Zv316na7XlX1lZWcrKypIkTZ48WZ7Lh8jEc4HuaDne5ootKlSqx+N0KACiTGxsrDz87EGInLRQNGTIkODfCwsLtXDhQv3kJz+RVD+JyjFJisejgrXLVJ7cRJ4BmTJxcXXwscNbccvzVPSfErkbJcrVONnpcABEEZIUoH5Ya7VkyRI1btxYxhi53W5JUnJysrZv367y8vI6XatNZmamMjMzg7dzCw9LOlxfHzksVTVNU9X+PcrJoasIQGh5PB5+9qBOtWjR4rj3nfIeRVu2bFFxcbG8Xm+9JirfT1IO7t0j/9IFMj0vU24Bx5FKkj8xSZKUu3WzzDmtHY4GQDQhSUF9OFGiEi2MMRo9erTeeecdZWdn68orr5QklZWVye/3KzExURUVFXW2htNj3B7ZDaudDgMAgHp1SqeeFRUVadq0afrVr34V+kRl3QqpvFSmx2Wn8/kikkk7cjX/EKduAAAQ7mbNmqX58+dLCuwNec0112jTpk2SpJ07d6pZs2Zq27Ztna7hNLm9UkGerK/S6UgAAKg3Jy0U+Xw+Pf/88xoxYoS8Xm/IExX/soVSSqrUvvNpf8iIc+R4VnuIq/oAAIS7zMxMLViwQOPHj5ff71fPnj21cOFCzZgxQ59//rm6deumHj161OkaTlOaR7JWyj/kdCQAANQbY621J3rAp59+qv/5n/9R69aBEaeBAwfqX//6lzp37qw1a9Zo4sSJkqTx48ef1lpSUtIJA/zmmj4yA4bIdeOdZ/xhI4X1V8n/q+EyVw2X69qRTocDIIoweob6wOjZsYqKirR27Vp17NhRqamp9bJ2Mnv37q2HTxbe7MbV8r8wXq5xk2TacRETQOiQg6GunSj/OmmhqDahTFS+Gdpdrof+KHPBRT80zIhW9dDtMu06y3X7WKdDARBFSFJQHygUNUwUio5l9+2W/w+/lrn9Prl6D3Q6HABRhBwMda1ONrM+WnJysvr27VtnayeU3kw6v8PphBnZ3F5Z9igCAAAIHTf7RAIAIt8pbWbtJNO9v4wxTofR4Bi3hyQFAAAghExCopTchBwMABDRGn6hqCenndXK7ZXycmU54hYAACB00jwcKAIAiGgNvlCklm2djqBhcnulKp9UmO90JAAAANHD7aWjCAAQ0Rp8oYixs9qZ6hn5PK5oAQAAhIpxe8i/AAARrcEXinAcbm/gT65oAQAAhI7bK5UUy5aWOB0JAAD1gkJRuDrSUWRzKRQBAACETPBiHV1FAIDIRKEoXCUlSwmJtD4DAACE0Hfj/1ysAwBEJgpFYcoYI7m9soyeAQAAhM6RjiJyMABApKJQFM7SPBKjZwAAAKHT1C0ZF6NnAICIRaEojJl0L6NnAAAAIWRiYqQ0NweKAAAiFoWicJbmkQrzZSsrnY4EAAAgeri9snQUAQAiFIWicFZ96gZdRQAAACFj0jx0FAEAIhaFojAWPHWDRAUAACB03IHxf+v3Ox0JAAB1jkJROOPUDQAAgNBzeySfTzpc4HQkAADUOQpF4SwtPfAnM/IAAAAhY6rH/8nBAAARiEJRGDPxCVKTpoyeAQAAhFKwUEQOBgCIPBSKwp3bK8tm1gAAAKFzZJ9Im0ehCAAQeSgUhTu3R8olSQEAAAiZxk2k+AQpl4t1AIDIQ6EozBm3VzqUI2ut06EAAABEBWOM5PZwoAgAICJRKAp3bo9UXiqVFjsdCQAAQPRweyXG/wEAEYhCUZgzbKYIAAAQcoGubvIvAEDkoVAU7tICmykyIw8AABBCaR6pIE+2stLpSAAAqFMUisJdeqCjiFM3AAAAQuhIDqb8XGfjAACgjlEoCncpqVJMDK3PAAAAIcT4PwAgUlEoCnPGFSOlpkuHGD0DAAAImSPj/5YcDAAQYSgURYJ0L8ezAgAAhJL7yD6R5GAAgAhDoSgCmDQPHUUAAAAhZOITpOQUcjAAQMShUBQJ3F4pP1fWX+V0JAAAANHDTVc3ACDyUCiKBG6PVFUlFeQ7HQkAAED0cHsZPQMARBwKRRGAUzcAAABCz7g9Uh6jZwCAyEKhKBIcKRRx6gYAAEAIub1SaYlsSbHTkQAAUGcoFEUCTt0AAAAIveocjK4iAEAEoVAUCRo1lhIbkaQAAACEEOP/AIBIRKEoAhhjAqdu5JKkAAAAhEz1+D85GAAgglAoihRuD1ezAAAAQqlpqhQTQ1c3ACCiUCiKEMbtJUkBAAAIIeOKkVLTuVgHAIgoFIoiRZpHOlwgW1HudCQAAADRI83DybMAgIhCoShSVG+mmJfrbBwAAABRxLi9dBQBACIKhaIIYdI5dQMAACDk0j1SXq6s3+90JAAA1AkKRZEizSNJshSKAAAAQifNK1X5pMJ8pyMBAKBOUCiKFEcKRWJGHgAAIGSMm65uAEBkiXU6ANQNExcnpaSSpAAAEGZKSkr04osvyu/3KyEhQWPHjtWYMWN01llnSZJGjRqlVq1a6b333tPq1at1/vnna/To0ZJ0RmuoI+4jF+vyciS1dzQUAADqAh1FkcTt5dQNAADCzMKFC/XTn/5Ujz76qFJTUzVr1iz169dPEyZM0IQJE9SqVStt27ZNmzZt0qRJk9S0aVOtXbv2jNZQh450FNlcLtYBACIDHUWRxO2V9u5yOgoAAPADDBkyJPj3wsJCpaena9WqVdqwYYNatWqlO++8Uxs3blSvXr1kjFGXLl20Zs0aJSUlnfZaRkbGMXFkZWUpKytLkjR58mR5PJ6QfQ/CmU1P18HEJDUqLVITvmcA6klsbCw/lxEyFIoiiHF7ZNevlLVWxhinwwEAAD/Ali1bVFxcrIyMDF1++eVKS0vTlClTtHr1apWVlQVH0ZKTk5Wfny+Xy3Xaa7XJzMxUZmZm8HZODl3Kp8qmpatk7zcq53sGoJ54PB5+LqNOtWjR4rj3USiKJG6vVFEulRRJjZs4HQ0AADhFRUVFmjZtmu6//36lpqYqLi5OktS2bVvt27dPiYmJqqiokCSVlZXJWntGa6hjbo/E6BkAIEKwR1EECZ66QaICAEDY8Pl8ev755zVixAh5vV699NJL2rFjh/x+v5YvX67WrVurbdu22rRpkyRp586d8nq9Z7SGumXcXg4UAQBEDApFkaT61A0SFQAAwsbcuXO1fft2ffjhh5owYYJatmypKVOmaNy4cWrXrp0yMjLUoUMH7dixQ9OnT9esWbPUv3//M1pDHXN7pMMFspUVTkcCAMAZM7aB9x/v3bvX6RDChi3Ik/+BW2VG3CXX5UOdDgdABGI+HvXhRDPy+E5FRYVWrVqlNm3aBPccOpO1kyEHO3X+JZ/JTv+zXBP/P5lm/PcMoO6Rg6GusUdRtGjSVIqJZfQMAIAIFB8fr969e9fZGuqOSfPIStKhHIlCEQAgzDF6FkGMyxVofc6j0gwAABAy6YF9nyzj/wCACEChKNK4vSQpAAAAoZTGPpEAgMhBoSjCmDQPSQoAAEAImbj4wBYAh+jqBgCEPwpFkcbtlfIPyVZVOR0JAABA9KCrGwAQISgURRq3R/L7pYJDTkcCAAAQPdweOooAABGBQlGEMe7AZookKgAAAKFj3F7pUI6stU6HAgDAGaFQFGncnLoBAAAQcm6vVF4qlRQ7HQkAAGeEQlGkcXPqBgAAQKiZ6hwsjxwMABDeKBRFGNMoSWrUmNEzAACAUKoe/88lBwMAhDcKRZHI7WH0DAAAIJSOdBRZOooAAGGOQlEkcnsZPQMAAAillDQpJpYcDAAQ9igURSDj9kh5tD0DAACEinG5pLR0Rs8AAGGPQlEkSvNIRYdly8udjgQAACB6uD2MngEAwh6FokiUfmQzRRIVAACAkDFuLweKAADCHoWiCGSqT91gRh4AACB00jxSfq6sv8rpSAAAOG0UiiJR2pFTN3IpFAEAAISM2ytVVUkF+U5HAgDAaaNQFInS0iVj2NAaAAAghEw6Xd0AgPBHoSgCmdi4wBGtJCkAAAChU93VzT5FAIAwRqEoUrk9JCkAAAChxD6RAIAIEHsqD8rPz9fzzz+vJ554QocOHdIjjzyi5s2bS5Luu+8+paSkaOrUqdq9e7e6deum4cOHS9Ipr6HuGbdXdvcOp8MAAACIGiapsZTYiPF/AEBYO2lHUVFRkf7yl7+ovLxckvTVV19p2LBhmjBhgiZMmKCUlBRlZ2fL7/dr4sSJOnDggPbt23fKa6gnbo906KCstU5HAgAAED3cXg4UAQCEtZN2FLlcLo0dO1bPPPOMpEChaN26dfrss8/+f/buO77K8vzj+Od+kjBCgOTkhBF22EuGG7UucNVq3a2jVeuodW+rtaAI4t57tI5aa63WVUUCDhyoPxURJLKDDEU2IZD1XL8/nrCUFTg5zxnf9+vlK8lzknMuMISL73Pf90W/fv04+eSTmTJlCnvvvTcA/fr1o6SkhNmzZ2/XtdatW2/yesXFxRQXFwMwatQootFo7H61aaS8XUdWVVWS3zALr1lu2OWISIrIzMzUz2URka2JFGjrmYiIJLVtBkXZ2dmbfNy/f3+OO+44GjZsyPDhwyktLaWi3D2BLwAAIABJREFUooJIJAJATk4Os2fP3u5rPzV48GAGDx68/uPFi7V0d0dYw8YALJn+La5D55CrEZFUEY1G9XNZYq6wsDDsEkRixkWiWOmMsMsQERHZYXU+zLp79+40btwYz/Po2LEjCxcupFGjRlRWVgKwdu1afN/f7mtST3SYooiIiEj8RQpg1QqssiLsSkRERHZInYOiESNGsGzZMioqKpg0aRLt27enqKiIkpISAEpLS2nRosV2X5N6UhsUafKZiIiISBytv1mnHkxERJLTdk0929jxxx/PDTfcQGZmJkOGDKGwsJDc3FyGDh3KsmXLmDhxIiNGjADY7mtSD5o2h8wsrSgSERERiSMXiWIQTD5r1SbsckREROrMWYzGYpWVlTFp0iR69epFbm5una5tzYIFC2JRXlqque5cXIcueOdcGXYpIpIidEaR1AedUZSY1IPtGPvxe/xrz8GdfhHePoO3/QUiIttBPZjE2tb6rzqvKNqSnJwcBg0atEPXpJ5ECjCtKBIRERGJn9z84K22nomISJKq8xlFkjxcXhSWKCgSERERiReXlQXN87T9X0REkpaColSWXwArlmHV1WFXIiIiIpI+tKpbRESSmIKiVJYXBfNhxdKwKxERERFJH3lRbT0TEZGkpaAohTmNZxURERGJOxcpgKU/EqOZMSIiInGloCiV5QdBkZY+i4iIiMRRJAqVFVBeFnYlIiIidaagKJXlRYO3CopERERE4mb9qm4NFRERkSSkoCiFuUaNITtHW89ERERE4mn99n8FRSIiknwUFKW6SFRbz0RERETiKRKs6rZlulknIiLJR0FRqqs9TFFERERE4qRpc8jM1NYzERFJSgqKUlwwdUN3s0RERETixXlecFakVhSJiEgSUlCU6iJRKC/D1q4JuxIRERGR9BEp0PZ/ERFJSgqKUt26wxR1R0tEREQkblwkqu3/IiKSlBQUpTiNZxUREREJQV4BLF+K1dSEXYmIiEidKChKdeumbuiOloiIiEj85EfB92HF0rArERERqRMFRamueQScp61nIiIiInHk8mpXdWuoiIiIJJnMsAuQ+uUyM6F5nraeiYiIJKjy8nLuvvtufN+nYcOGXHrppTz22GPMmzePgQMHctxxxwHw0EMPxfSa1LPa7f+29EccPUMuRkREZPtpRVE6yC/AtKJIREQkIY0fP54jjzySv/zlL+Tm5vLhhx/i+z4jRozghx9+YOHChXzyyScxvSZxULv9Xwdai4hIstGKojTgIgVY6YywyxAREZHNOPTQQ9e/v3LlSsaPH88RRxwBQL9+/SgpKWH27NnsvffeMbvWunXrn9VRXFxMcXExAKNGjSIajdbfLzpNLMrOodGa1TTT76WI7KTMzEz9XJa4UVCUDvKi8OUEzAznXNjViIiIyGZMmzaN1atXU1BQQCQSASAnJ4fZs2dTUVER02ubM3jwYAYPHrz+48WLtRp5Z1lePmvmz6VSv5cispOi0ah+LktMFRYWbvExbT1LB5ECqK6CVSvCrkREREQ2o6ysjCeffJLzzjuPRo0aUVlZCcDatWvxfT/m1yROIgUaKCIiIklHQVEacNojLyIikrCqq6u58847OfnkkykoKKCoqIiSkhIASktLadGiRcyvSXy4SFT9l4iIJB0FRekgsm48qxoVERGRRDNu3Dhmz57NSy+9xLBhwzAzxo8fz1NPPcXHH3/MwIED2X333WN6TeIkUgBlq7CKirArERER2W7OzCzsIrZmwYIFYZeQ9GzVSvzLTsWddBbe4KPCLkdEkpj2x0t92Noe+XRVVlbGpEmT6NWrF7m5ufVybVvUg+08f8I72BN34Q1/ENeqbdjliEgSUw8msba1/kuHWaeDnKaQ1UArikRERJJETk4OgwYNqtdrUv9cpACDoAdTUCQiIklCW8/SgHMuWPq8VAm0iIiISNzUbv839WAiIpJEFBSli0gU04oiERERkfjJzQfntKpbRESSioKiNBFM3dDdLBEREZF4cZmZ0DxPQZGIiCQVBUXpIlIAK5dh1VVhVyIiIiKSPvKi2nomIiJJRUFRusiLghksWxJ2JSIiIiJpw+mcSBERSTIKitKEyw8OU2SZGhURERGRuMkvgKU/YmZhVyIiIrJdFBSli/VTN7RHXkRERCRu8qJQVQllq8KuREREZLsoKEoXebUripYoKBIRERGJF1d7s04HWouISLJQUJQmXMOGkNNUW89ERERE4ikSDd4uU1AkIiLJQUFROtHUDREREZH4Wrf9f4l6MBERSQ4KitJJpEDLnkVERETiqWlzyMxSDyYiIklDQVEa0XhWERERkfhyzgXbz7T9X0REkoSConQSicKa1dia8rArEREREUkfkQJNnhURkaShoCidrJ+6oTtaIiIiIvHi8qLqv0REJGkoKEojbt3UDd3REhEREYmf/AJYvhSrrg67EhERkW1SUJRO1k3dUFAkIiIiEj+RAjAfViwNuxIREZFtUlCUTppHwPO09FlEREQkjlzeulXd6sFERCTxKShKIy4jA3Ij2nomIiIiEk/5WtUtIiLJQ0FRuokUYBrPKiIiIhI/WlEkIiJJREFRmnGRAq0oEhEREYkj16gxZOeoBxMRkaSgoCjd1I5nNd8PuxIRERGR9BEp0NYzERFJCgqK0k1+AdRUw6oVYVciIiIikj4iUW09ExGRpKCgKM1smLqhO1oiIiIi8aLt/yIikiwUFKWbSDB1Q42KiIiISBxFolBehq1dE3YlIiIiW6WgKN2sH8+qpc8iIiIicbPuZp2mz4qISIJTUJRusnOgQUOtKBIRERGJI7cuKFqiHkxERBKbgqI045yrnbqhu1kiIiIicRMJzok0rSgSEZEEp6AoHUWiWlEkIiIiEk/NI+A89WAiIpLwFBSlIU3dEBEREYkvl5kJuRHQqm4REUlwCorSUaQAVi7HqqrCrkREREQkfUSimG7WiYhIglNQlI5q98hr6oaIiIhI/GhVt4iIJAMFRWnIaTyriIiISPzlRWHpYsws7EpERES2SEFROqoNikzjWUVERETiJ1IA1VWwakXYlYiIiGyRgqJ0lJcfvNXSZxEREZG4cfm12//Vg4mISAJTUJSGXIOG0LS5tp6JiIiIxFNe7fZ/TT4TEZEEpqAoXeVp6oaIiIhIXK3b/q8eTEREEpiConQVKQCdUSQiIiISPzlNIauBVnWLiEhCU1CUplx+gaZuiIiIiMSRc04360REJOEpKEpXeVGoWANrVoddiYiIiEj6iGj7v4iIJDYFRekqosMURUREROLNRaLaeiYiIglNQVGachGNZxURERGJu0gBrFiGVVeFXYmIiMhmKShKV5q6ISIiIhJ/eVEwg+VLw65ERERksxQUpavmuZCRoa1nIiIiInHk8tdt/9fNOhERSUyZYRcg4XBeBuTmq0kRERFJEMuXL+fOO+/kxhtvZOnSpVx77bW0atUKgMsuu4xmzZrx0EMPMW/ePAYOHMhxxx0HsFPXJAQbrep2IZciIiKyOQqK0lkkiukwRRERkdCVlZXxwAMPUFFRAcD06dM59thjOeSQQ9Z/zieffILv+4wYMYIHH3yQhQsXMnfu3B2+1rp1601qKC4upri4GIBRo0YRjUbj9xuQRqxpDouAJhVraKLfYxHZTpmZmfq5LHGjoCiNuUgBNmNq2GWIiIikPc/zuPTSS7n11luBICj6+uuvGTt2LP369ePkk09mypQp7L333gD069ePkpISZs+evcPXfhoUDR48mMGDB6//ePFi3UyqNzlNWf3dHNbo91hEtlM0GtXPZYmpwsLCLT62XUHRxkuhq6uruf3221m9ejUHHnggBx100E5dkxBForB8CebXBFvRREREJBTZ2dmbfNy/f3+OO+44GjZsyPDhwyktLaWiooJIJAJATk4Os2fP3qlrEqK8KKZzIkVEJEFt8zDrny6FfuuttygqKmL48OF88sknrFmzZqeuSYgiBVBTAyuXh12JiIiIbKR79+40btwYz/Po2LEjCxcupFGjRlRWVgKwdu1afN/fqWsSokiBzokUEZGEtc0VRT9dCj1lyhROOeUUAHr27MnMmTN36lqfPn02eT3tj4+fig6dWQ40r6migX6fRWQ7aH+8SHyMGDGCiy++mOzsbCZNmsSQIUOoqKigpKSEbt26UVpaSmFhIfn5+Tt8TcLjIgXYtClhlyEiIrJZ2wyKfroU+qdLl1esWLFT135K++Pjx7IaALB81gy8/FYhVyMiyUD746U+KLT4ueOPP54bbriBzMxMhgwZQmFhIbm5uQwdOpRly5YxceJERowYAbBT1yQkkSisWY2tKcc1zt7254uIiMRR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Jv3iF79QfX29Jk2apBtvvFHWWqWkpEiS2rZtq9raWt1www2aMmVK5LkPPfSQ+vTpo379+unXv/61Vq1apX79+unuu+/Whx9+eFTMH330UeR5ixYtUllZ2VFxvPvuu/rpT396wkJR+/bt9fzzz+u9995TcnKyUlJS9NhjjykpKUllZWVavHix+vTpc9znAwCAxEEOdmwO1pR//OMfKioqOuFjyMEA5yQ7HQCAlrV9+3b95je/UUpKigYMGNDkY4LBoGprayMzRpLUpk0bjRs3Tq+++mqTz/F6vcrIyDhmfP369erWrZsGDRoUGSspKVFRUZH+4z/+Q8uWLZMkJScnR+K59NJLlZ+frzvuuEM7duzQ66+/rn79+um9995T586dJUkej0e/+c1vlJmZqenTp0de+6677tKvf/1rJScna9asWXrggQdUWFioV199VQUFBXr99dclSd/85jcVDAYjz5syZYqSkpL0/vvvyxgjSZoxY4buuusutWnT5ri/z507d+rOO++UMUY1NTXauHGjsrKy5Pf7tXDhQg0ePFh+v/+4zwcAAImBHKzpHKwpycnJ8vl8J3wMORjgHApFgItUVFRo3Lhxuu666/T888+f0nPbtm170sc0zjQ1GjRokNatW6fa2lqlp6dLkmbNmqVFixYpPT1d//7v/y5Jqq2tVVlZmfbu3StJstbq4osv1rJlyyJFmyVLluhb3/pWZHbJGKO7775bkyZNOuq6ixYt0i233CJJqqqqUklJifr166eDBw+qqqpK/fr1kyTt2LFDNTU1kee9/vrrGjx4sB544AFNnjxZ69evV2FhoT755BPdddddkcfV1NRo7Nix+tvf/iZJeuutt/SPf/xDGzdu1Pbt2/Xqq6/K6/XqgQce0MCBA7V69Wr16NFDUni9/k033aRHH320ub92AADgAuRgx8/BmmKtVXV19QkfQw4GOIdCEeAS1dXV+s53vqNevXpp/PjxSktLU1ZWlmpra4/qmKmurtbw4cOPWbtujNE777xz3LXehw4dOmasvr5eH3zwgUaPHi0pPIOUlJSk559/Xi+//LKuvvpqSdLatWuVl5cnKZw85OXl6cEHH9S1114rKdymfccdd0iSQqGQpPDsWaM///nPkdfavXu30tPTVVBQoOnTp2v27Nl644039Je//EVz5849Kjlr37595PtAIKA//elPuvrqq/Xzn/9c9957r+688049/vjjR72nQYMGReKSpN/+9reaMGGCxowZox49eigvL0/nn3++xo8fH5mB+853vqPf//73Wr16tR566KEmf38AAMCdyMFOnIM1ZdeuXcrMzDzhY8jBAOdQKAJcIjU1VY8//riGDRumv/3tb/rBD36gV155RePGjdM555yj+++/Xx6PR2+88YY++OCDJl/jZG3PX5eUlHTM2GuvvSaPx6Mrr7wyMhYMBpWamipJ6tatm8aNG6fx48frl7/8pZ588kl5PB4NGjRI8+fPP+b1unTpouTkr25VO3fu1OrVqzVixAiVlJSorq5OI0aMiMxmjRgx4qjnz58/X4FAQJI0evRorV+/XkuXLtWHH36o4uJirVmzRj/96U/15ptvqqqqSl988YW+973vRZ5fWFioG264QU888YSeeuopdenSRT/72c9UV1entWvX6uDBg5LCG2N37NjxmBk/AADgbuRgJ8/BjlRXV6dVq1appKRE1tpIZ9PXkYMBzmEza8BFRo4cqZSUlMg/mJL04osvatasWfrwww8lhWelsrKyJIXbfhvV1dW1SAzXXnutXnrpJd14443avn175LUb26qNMXrooYf0yiuvRGaoGpOdYDB4zH9H/rkk3Xnnndq6datyc3Pl8/n0xRdfqLi4WA8//LCuvPJKFRcXa+nSpZo2bZrWrl0bacdu1LFjR/Xs2VN//OMf5ff7VV9fH0lkjDGaPn165HdXX1+v559/Xo8//rjGjBmjAQMGaNSoUXrxxRf1zjvvyOv1auXKlZLCSUqvXr1a5HcIAADiCznYyXOwRosWLVJKSooyMzM1c+bMJh9DDgY4i44iwEUuu+wyLV26NLLm+7XXXlN9fb2MMfrnf/5nSVJlZaWstXr55Zd111136Xe/+52k8HGpf/3rX5Wfn9/kax+56eKRxo4dG0kiqqqq5PV6NWjQIB0+fFiPPvqonnrqKVVXV0dmsxrdfPPNRyVJCxYsOOlM0LvvvqvXXntNH330kSorK9WzZ0995zvficTfuD7eWqs+ffpo6tSpR123vr5eF110kaZPn67vfve7ksKtz9ZaVVZWqlevXvqXf/mXyOOTkpL00ksvKTk5WY8++qi2b9+u888/X+eff77++te/6oEHHtA777wjSSouLo78jgEAQGIhBztxDnakl156Sdddd51GjRqlKVOmaOzYscd0FZGDAQ6zAFznV7/6lX3hhRestdbm5ubaBx54wNbW1lprrb3nnnvsk08+ecxzfvrTn9pHHnnkuK+ZmZlpN2/efNTYwIED7Zw5cyI/9+rVyy5dutRaa+3cuXNt+/btbVlZmZ0zZ4698MILj3ruzJkz7QUXXGBDoZD905/+ZEeNGtXkdTt37mxnzpxprbV2zpw5dsqUKfZ///d/7cCBAyOPmT17tl23bp211trNmzfb493aXn75ZdurVy9bVVUVGZs8ebKVZP/61782+Zzc3FzbsWNHK8l27NjRdu7c2SYnJ9sXXnjBVlZWWq/Xa3fv3m0zMzOPel0AAJB4yMFO/H8vi4uLbVpamv3ss8/s4cOHbbdu3ewf/vCHJh9LDgY4h6VngAvt2bMncgrEW2+9pc8++0xz586VFG577tChwzHPWbRokYYNG9ZiMVx88cW6+eabVVFRocrKymOOdX3jjTc0atSoyAxSUVGR0tPTj/mv8ZQOKbzH0NSpUyNt21K4dfsnP/mJ3nrrraNev76+/qifq6qqdN999+nJJ59Uu3btImMvv/yy/vM//1P33Xdfkyd0FBYW6u2339agQYO0Z88erVixQhkZGbr22muVlpam73//+7rhhhs0bNiwyOsCAIDERA52bA7WqK6uTj/5yU/04x//WEOGDFFqaqr+8Ic/6Fe/+pWWLl16zOPJwQDnsPQMcKGNGzfqxhtvPKqNeOHChZLC7cvJycl68cUXI8egLl++XNu3b9eFF17YonE899xzksL/0B95ssXOnTv1xhtvaMmSJZLCiUZOTs5xN1L8uiMLOi+++KJKS0v1k5/8RFOmTNGFF16oyy+/XHV1dUetq7/77rvVt29fjRs3TlL4ZI9bb71VF110ke6++24VFRVp4sSJ+p//+R+lpaUddb3CwkKVl5drwoQJOnjwoH7wgx9EEqXbbrtNF110kV577bXT/TUBAACXIAc7NgeTpNraWl133XWqrKzUww8/HBm/8sordfPNNysvL09vv/22cnNzj3oeORjgDDqKABdauHChSktLtXv37sh/q1ev1vvvv6+ePXtq5syZmj17tqRwwWTSpEm65ZZbjjrZQgpvbLhs2TJ9+OGHKi8vP2ateTAY1GWXXabU1FSlpqZq69atkc0Pj7Rs2TJ17tw58vOdd96pXr16acCAAZKannkqLy/XkiVLVFlZecy69ZycHD344IO69dZbdccdd+gPf/iDQqGQVq9ere9+97s6fPiw8vPzI8e8/v3vf9f06dP1+9//XlJ408Orr75a69ev10svvSRJ+tOf/qS9e/cqJydHa9asOep699xzj9asWaP6+nrt27dPM2fO1L333qt9+/bpd7/7nfr376+HH35YO3fuPPn/OAAAwLXIwY7OwaRwMeziiy/WunXr9NFHHx3T4fTss8/qmmuu0ZgxY3TnnXdqz549kT8jBwOcQaEISBDbtm3T5ZdfrksuuUQ5OTmRFt3XX39dGzdu1N13333Mc5KTk/XjH/9YEydO1IQJE46ZWWrTpo1mz56t6upqVVdX67LLLovMIIVCIY0fP179+vXT+++/r9tuu02SVF1drSFDhujmm2+OvE7jxo9HSklJ0TXXXKNzzz1XQ4cOlRROZgYMGCCv16sbbrhBFRUVWrx4sa6//np17txZb775pjZu3Kj+/fvrhhtuiMyW5eXlacaMGTr77LP10ksvqV+/fmrXrp1mz54d6R5KT09Xfn6+vvnNb+rcc8/VG2+8IUnasGGDHn/8cQ0ePFg9e/ZUUVGRVq1apZSUFJ133nnKzc3VypUrdcEFF2jo0KF67733zuh/JwAA4C6JnIPt3btXeXl56t27txYtWhQ5Ee5IHo9HL774ol544QW9/fbbkaIPORjgHGPtEVveA0hIVVVVxyy3alRXV3fSkzCOZ+XKlfL7/erWrdtpPb+pkzq++OILeTwe9e3b95jZtyOVl5cfM2MlSevWrdPy5ct13XXXHfe5b731lq666iqlpKTonXfe0fz583X77bcrOztbUvh0j1/96le67bbbInsKWGv19NNPa+zYserTp8/pvF0AAJBgEiEH27Vrl7p27dqs6waDwchrk4MBzqFQBAAAAAAAAEksPQMAAAAAAECDpKlTp051OggAAAAcq6ysTA899JAuueQSBYNBPfLII/rwww8lSb179z6jMQAAgKYcf3HpEcrKyvTEE0/ovvvuU0lJiZ555hkZY9SlSxfdeuutqq+v12OPPabKykpdcsklGjNmjILBYLPGToYd7AEgdgQCAZWUlDgdBlzmdPfQcLuKigo9++yzkeOo8/PzlZ2drYkTJ+rhhx9WTk6OZs2addpjjRvqHg85GADEDnIwtLQT5V8nLRR9PUn5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\n",
      "text/plain": [
       "<Figure size 1440x1080 with 4 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# 用户整体消费趋势分析（按月份）\n",
    "# 按月份统计产品购买数量，消费金额，消费次数，消费人数\n",
    "plt.figure(figsize=(20,15)) #单位时英寸\n",
    "# 每月的产品购买数量\n",
    "plt.subplot(221)  #两行两列，占据第一个位置\n",
    "df.groupby(by='month')['order_products'].sum().plot()  #默认折线图\n",
    "plt.title('每月的产品购买数量')\n",
    "# 每月的消费金额\n",
    "plt.subplot(222)  #两行两列\n",
    "df.groupby(by='month')['order_amount'].sum().plot()  #默认折线图\n",
    "plt.title('每月的消费金额')\n",
    "# 每月的消费次数\n",
    "plt.subplot(223)  #两行两列\n",
    "df.groupby(by='month')['user_id'].count().plot()  #默认折线图\n",
    "plt.title('每月的消费次数')\n",
    "# 每月的消费人数（根据user_id进行去重统计，再计算个数）\n",
    "plt.subplot(224)  #两行两列\n",
    "df.groupby(by='month')['user_id'].apply(lambda x:len(x.drop_duplicates())).plot()  #默认折线图\n",
    "plt.title('每月的消费人数')\n",
    "#分析结果：\n",
    "# 图一可以看出，前三个月销量非常高，而以后销量较为稳定，并且稍微呈现下降趋势\n",
    "# 图二可以看出,依然前三个月消费金额较高，与消费数量成正比例关系，三月份过后下降严重，并呈现下降趋势，思考原因？1：跟月份有关，\n",
    "# 在我国来1，2，3月份处于春节前后。2.公司在1，2，3，月份的时候是否加大了促销力度\n",
    "# 图三可以看出，前三个月订单数在10000左右，后续月份的平均消费单数在2500左右\n",
    "# 图四可以看出，前三个月消费人数在8000~10000左右，后续平均消费消费在2000不到的样子\n",
    "# 总结：所有数据显示，97年前三月消费事态异常，后续趋于常态化"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 用户个体消费分析"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1.用户消费金额，消费次数(产品数量)描述统计"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "           order_dt  order_products  order_amount\n",
      "count  2.357000e+04    23570.000000  23570.000000\n",
      "mean   5.902627e+07        7.122656    106.080426\n",
      "std    9.460684e+07       16.983531    240.925195\n",
      "min    1.997010e+07        1.000000      0.000000\n",
      "25%    1.997021e+07        1.000000     19.970000\n",
      "50%    1.997032e+07        3.000000     43.395000\n",
      "75%    5.992125e+07        7.000000    106.475000\n",
      "max    4.334408e+09     1033.000000  13990.930000\n",
      "用户数量: 23570\n"
     ]
    }
   ],
   "source": [
    "user_grouped = df.groupby(by='user_id').sum()\n",
    "print(user_grouped.describe())\n",
    "print('用户数量:',len(user_grouped))\n",
    "# 从用户的角度：用户数量23570个，每个用户平均购买7个CD，但是中位数只有3，\n",
    "#  并且最大购买量为1033，平均值大于中位数，属于典型的右偏分布(替购买量<7的用户背锅)\n",
    "# 从消费金额角度：平均用户消费106，中位数43，并且存在土豪用户13990，结合分位数和最大值来看，平均数与75%分位数几乎相等，\n",
    "# 属于典型的右偏分布，说明存在小部分用户（后面的25%）高额消费（这些用户需要给消费金额<106的用户背锅，只有这样才能使平均数维持在106）"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x2a9968a1288>"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#绘制每个用户的产品的购买量与消费金额散点图\n",
    "df.plot(kind='scatter',x='order_products',y='order_amount')\n",
    "# 从图中可知，用户的消费金额与购买量呈现线性趋势，每个商品均价15左右\n",
    "# 订单的极值点比较少（消费金额>1000，或者购买量大于60）,对于样本来说影响不大，可以忽略不记。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.用户消费分布图"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x2a996924ac8>"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAtsAAAEGCAYAAAC0OFnEAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjMsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+AADFEAAAgAElEQVR4nO3da3hU5bn/8d9MhhBCgBASwCABwkFIMaER5SBVqAO4udjSP8HaInW3iF7WQy21iLZAAggGpBQqhwoFil5VRMvGU8UaUYkiEAtpSmIKQg4CMRggxMlpmMz8X6TMNiecHFayhnw/b2TuWbPmfkK8182znrWWxePxeAQAAACgxVnbOgEAAADgakWzDQAAABiEZhsAAAAwCM02AAAAYBCabQAAAMAgNNsAAACAQWi2AQAAAIPYjP4Ch8OhkydPqn///uratavRX1fDmTNnGv2Z8PBwFRUVGZBNyyNXY5CrMci1cSIjI9v0+9tKY+u2Gf6ujHA1jutqHJPEuPyJkWO6Us02tNl2OBxKTk5WfHy8tm/frsTERM2fP1+9evWSJM2ePVtRUVHauXOnjhw5ooEDB2rOnDmS5HMMAAAAMCtDm+38/Hzdc889GjJkiBwOh/bu3aubb75Zs2bN8m5z8uRJZWdna/ny5Xr11VeVkZGhkJAQn2KxsbFGpg8AAAA0i6HNdkxMjCQpKytLJ06c0KhRo3T48GFlZmYqKipK999/v7KysjRq1ChZLBbFxcUpPT1dwcHBPsVqN9spKSlKSUmRJCUnJys8PLzROdtstiZ9ri2QqzHI1RjkCgBojwxfs+3xeLR//3517txZAwYM0MKFC9W9e3etW7dOR44cUUVFhXdZSUhIiIqLi2W1Wn2K1Wa322W3272vm7Iux5/WKJGrMcjVGOTaOO11zTYAXG0MvxuJxWLRnDlzFBUVpQsXLqh79+6SpOjoaBUUFCgoKEhOp1OSVFFRIY/H43MMAAAAMDNDm+3du3frww8/lCSVlZVp8+bNys3NldvtVlpamvr166fo6GhlZ2dLkvLy8hQREeFzDAAAADAzQ5ttu92uffv2KTExUW63W4sXL9a6des0b948DRkyRLGxsRo6dKhyc3O1bds27d69W+PGjfM5BgAAAJiZxWOC9RhOp1OHDx/WgAEDvOuyfY1dCffZNg9yNQa5GsMMubbXNdvcZ7va1Tiuq3FMEuPyJ1flfbZ9FRgYqNGjRzcp1tIK/9/YeuMBm1839HsBAI1HzQZgdjyuHQAAADAIzTYAAABgEJptAAAAwCA02wAAAIBBaLYBAAAAg9BsAwAAAAah2QYAAAAMQrMNAAAAGIRmGwAAADAIzTYAAABgEJptAAAAwCA02wAAAIBBaLYBAAAAg9BsAwAAAAah2QYAAAAMYmvrBAAA5lBWVqY1a9bI7XarY8eOmjt3rjZv3qxTp04pPj5eCQkJkqSNGzc2OQYA7Q0z2wAASVJqaqqmTp2qBQsWKDQ0VB9//LHcbreWLVumwsJCFRQU6ODBg02OAUB7xMw2AECSNHnyZO+fS0pKlJqaqilTpkiS4uLilJ2drZycHI0ZM6ZJsWuuuaaVRwQAbY9mGwBQw7Fjx1RaWqqIiAiFhYVJkkJCQpSTk6PKysomx+qTkpKilJQUSVJycrLCw8MblWthA/HG7sdsbDab34+htqtxTBLj8idtNSaabQCAl8Ph0NatW/XYY4/pzTfflNPplCRVVFTI7XYrKCioybH62O122e127+uioqIWGUdL7aethIeH+/0YarsaxyQxLn9i5JgiIyMbfM/wNdsOh0MZGRkqKSkx+qsAAM3gcrm0evVqzZw5UxEREYqOjlZ2drYkKS8vTz179mxWDADaI0Nnth0Oh5KTkxUfH6/t27crMTFRf/nLX7iyHQBMaO/evcrJydGuXbu0a9cujR8/Xqmpqbpw4YLS09O1bNkySVJiYmKTYwDQ3hjabOfn5+uee+7RkCFD5HA4dPToUe/V6Rs2bFBBQYHy8/ObHONiGwBoOZMmTdKkSZNqxEaOHKmMjAxNmzZNwcHBkqqb6KbGAKC9MbTZjomJkSRlZWXpxIkTcjgcTb6KnSvbAaD1hYSEaOzYsS0WA4D2xvALJD0ej/bv36/OnTvLYrEYemV7c69ql/zrynZ/ulKYXI1Brsbwp1wBAOZmeLNtsVg0Z84c7dixQwcPHtRtt90myZgr2426qr2l99VS/OlKYXI1Brkawwy5XunKdgCA/zD0biS7d+/Whx9+KKn6McDTpk3jynYAAAC0G4Y223a7Xfv27VNiYqLcbrduuukmpaamavv27frkk08UHx+vG2+8sckxAAAAwMwMXUYSEhKihQsX1og15yp2rmwHAACAP2n1J0hyZTsAAADaC8OfIAkAAAC0VzTbAAAAgEFotgEAAACD0GwDAAAABqHZBgAAAAxCsw0AAAAYhGYbAAAAMAjNNgAAAGAQmm0AAADAIDTbAAAAgEFotgEAAACD0GwDAAAABqHZBgAAAAxCsw0AAAAYhGYbAAAAMAjNNgAAAGAQmm0AAADAIDTbAAAAgEFotgEAAACD0GwDAAAABqHZBgAAAAxCsw0AAAAYxGbkzsvKyrRmzRq53W517NhRc+fO1SOPPKJevXpJkmbPnq2oqCjt3LlTR44c0cCBAzVnzhxJ8jkGAAAAmJWhM9upqamaOnWqFixYoNDQUO3evVs333yzkpKSlJSUpKioKJ08eVLZ2dlavny5unXrpoyMDJ9jAAAAgJkZOrM9efJk759LSkrUo0cPHT58WJmZmYqKitL999+vrKwsjRo1ShaLRXFxcUpPT1dwcLBPsdjY2Brfl5KSopSUFElScnKywsPDG51zYQPxpuzLaDabzZR51YdcjUGuxvCnXAEA5mZos33ZsWPHVFpaqtjYWE2YMEHdu3fXunXrdOTIEVVUVHiXlYSEhKi4uFhWq9WnWG12u112u937uqioqMXG0JL7ainh4eGmzKs+5GoMcjWGGXKNjIxs0+8HALQMw5tth8OhrVu36rHHHlNoaKg6dOggSYqOjlZBQYGCgoLkdDolSRUVFfJ4PD7HAAAAADMzdM22y+XS6tWrNXPmTEVEROjZZ59Vbm6u3G630tLS1K9fP0VHRys7O1uSlJeXp4iICJ9jAAAAgJkZ2mzv3btXOTk52rVrl5KSktS3b1+tW7dO8+bN05AhQxQbG6uhQ4cqNzdX27Zt0+7duzVu3DifYwAAAICZGbqMZNKkSZo0aVKN2J133lnjtdVq1cKFC3X48GFNmTJFPXv2lCSfYwAAAIBZtcoFkt8mMDBQo0ePblIMAAAAMCueIAkAAAAYxBQz2wAAcyguLtbq1au1ZMkSnT9/Xr/5zW/Uu3dvSdKvfvUrde3aVRs3btSpU6cUHx+vhIQESfI5BgDtDTPbAABJ1bdqXb9+vSorKyVJx48f1/Tp071P/e3atasOHjwot9utZcuWqbCwUAUFBT7HAKA9otkGAEiqvmB97ty56tSpk6TqZvu9997T/Pnz9eKLL0qSMjMzNWbMGElSXFycsrOzfY4BQHvEMhIAgCQpODi4xusRI0YoISFBHTt21NKlS5WXl6fKykqFhYVJqn6ab05Ojs+x+qSkpCglJUWSlJycrPDw8EblXNhAvLH7MRubzeb3Y6jtahyTxLj8SVuNiWYbAFCv6667zvvU3/79+9f71F+32+1zrD52u112u937uqioqEVyb6n9tJXw8HC/H0NtV+OYJMblT4wcU2RkZIPvsYwEAFCvZcuW6cKFC6qsrFRGRoaioqLqPM23Z8+ePscAoD1iZhsAUK8ZM2Zo8eLFstlsmjhxoiIjIxUaGqrExERduHBB6enpWrZsmST5HAOA9oZmGwBQQ1JSkiRp+PDhWrNmTY33goODlZiYqIyMDE2bNs27ztvXGAC0NzTbAIBGCQkJ0dixY5sUA4D2hmbbR1X33VEnFrD59TbIBAAAAP6CCyQBAAAAg/jcbB84cMB7GycAgLlRswHAHHxeRvLRRx9py5YtiomJ0ZgxYxQfH6/AwEAjcwMANBE1GwDMwedm+9e//rUuXbqko0eP6tNPP9WOHTsUFRWlMWPG6MYbb5TNxvJvADALajYAmEOj1mzbbDZ17NhRHTp0UFVVlS5cuKCMjAw99dRTRuUHAGgiajYAtD2fpzY2bNig9PR09enTR6NHj9aSJUvUvXt3VVVV6f777zcyRwBAI1GzAcAcfG62hwwZolmzZqlr16414gEBAdqyZUuLJwYAaDpqNgCYg8/LSOx2uzp27ChJKi4u1sWLFw1LCgDQPNRsADAHn5vt1NRU76nH7OxsPf7449q/f79hiQEAmo6aDQDm4HOz/dJLL2nVqlWSpNGjR+vpp5/WSy+9ZFhiAICmo2YDgDk06t5PISEh3j8HBQWpqqrqituXlZVpzZo1crvd6tixo+bOnavNmzfr1KlTio+PV0JCgiRp48aNTY4BAOrX2JoNAGh5Pjfbt99+uxYtWqTvfe97kqofmDB58uQrfiY1NVVTp05VbGysNm/erI8//lhut1vLli3Thg0bVFBQoPz8/CbHrrnmmuaNHgCuUk2p2QCAludzs33HHXeof//+Sk9PlyTNmjVLsbGxV/zMNwt7SUmJUlNTNWXKFElSXFycsrOzlZOTozFjxjQpVrvZTklJUUpKiiQpOTlZ4eHhvg7Pq7AR2zZl/y3JZrO1eQ6+IldjkKsx/CnXhjSlZgMAWl6jlpF07dpVI0eO9L7OyspSTEzMt37u2LFjKi0tVUREhMLCwiRVn97MyclRZWVlk2O12e122e127+uioqLGDK/RjN7/twkPD2/zHHxFrsYgV2OYIdfIyMhm76OpNRsA0HJ8brZXr16t7Oxs9enTp0Y8MTHxip9zOBzaunWrHnvsMb355ptyOp2SpIqKCrndbgUFBTU5BgCoX1NrNgCgZfncbGdmZmrDhg3e+7b6wuVyafXq1Zo5c6YiIiIUHR2t7OxsDRkyRHl5eYqMjFSPHj2aHAMA1K8pNRsA0PJ8vvVfXFycMjMzG7XzvXv3KicnR7t27VJSUpI8Ho9SU1O1fft2ffLJJ4qPj9eNN97Y5BgAoH5NqdkAgJbXqDXbq1ev1sCBA9WrVy9v7MEHH2xw+0mTJmnSpEk1YiNHjlRGRoamTZum4OBgSdWnNZsaAwDUr7E1GwDQ8nxutmNjY1vkSvaQkBCNHTu2xWIAgLpaqmYDAJrH52Z7/PjxKikp0ZkzZzRo0CCdPn1a/fr1MzI3AEATUbMBwBx8XrO9d+9ePf7441qxYoVcLpdWrVqlt956y8jcAABNRM0GAHPwudl++eWXtWLFCnXo0EFBQUFauXIlhRsATIqaDQDm4HOzHRgYKJvNJovFIkmqrKyU1erzxwEArYiaDQDm4POa7enTpysxMVHl5eX605/+pPT0dCUkJBiZGwCgiajZAGAOPjfbEyZM0ODBg3X06FF5PB5NnjxZffv2NTI3AEATUbMBwBx8brazsrIkSVFRUZKkr7/+WllZWYqJiTEmMwBAk1GzAcAcfG62X3nlFUmSx+PR+fPnVVhYqKFDh2rx4sWGJQcAaBpqNgCYg8/NdmJiYo3Xhw8fVnp6eosnBABoPmo2AJhDky9Nj4+P1xdffNGSuQAADELNBoC24fPM9oYNG2q8PnfunNxud4snBABoPmo2AJiDz8127YtqgoODNWLEiBZPCADQfNRsADAHn5vt4cOH14mVlJR4/xweHt4yGQEAmo2aDQDm4HOz/dvf/lbFxcUKCQmR2+1WWVmZwsLCZLVaZbFYtG7dOiPzBAA0AjUbAMzB52Z7yJAhuvXWWzVy5EhJ0qFDh/TJJ5/o0UcfNSw5AEDTULMBwBx8vhvJsWPH9N3vftf7Oj4+3vvQBACAuVCzAcAcfJ7Z/u53v6ukpCSNGjVKHo9HBw8e1A033GBkbgCAJqJmA4A5+Nxs33///dq/f78+//xzSdKUKVM0ZswYwxIDADQdNRsAzMHnZttqtSo2Nlbh4eEaNGiQTp8+LYvFYmRuAIAmak7NLi4u1urVq7VkyRK5XC6tWrVKpaWlmjBhgr7//e83KwYA7Y3Pa7b37t2rxx9/XCtWrPAW0LfeesvI3AAATdTUmu1wOLR+/XpVVlZKkvbs2aPo6GgtXbpUBw8eVHl5ebNiANDe+Nxsv/zyy1qxYoU6dOigoKAgrVy5kmYbAEyqqTXbarVq7ty56tSpkyQpMzNTY8eOlSQNGzZMJ06caFYMANobn5eRBAYGymazeU9DVlZWymr99l79m6cjz58/r9/85jfq3bu3JOlXv/qVunbtqo0bN+rUqVOKj49XQkKCJPkcAwDU1dSaHRwcXON1ZWWlwsLCJEkhISG6ePFis2K1paSkKCUlRZKUnJzc6IftFDYQ9/eH9thsNr8fQ21X45gkxuVP2mpMPjfb06dPV2JiosrLy/WnP/1J6enp39rw1j4defz4cU2fPl2TJk3ybnPw4EG53W4tW7ZMGzZsUEFBgfLz832KXXPNNU0cNgBc3ZpSs+sTFBQkp9Op4OBgVVRUKCgoqFmx2ux2u+x2u/d1UVFRs8bd0vtpK+Hh4X4/htquxjFJjMufGDmmyMjIBt/zeRnJhAkT9Mtf/lIzZ85Unz59NH/+fE2YMOGKn6l9OvL48eN67733NH/+fL344ouSqk9RXr5CPi4uTtnZ2T7HAAD1a0rNrk90dLS33ubm5ioiIqJZMQBob3ye2Zaka6+9Vtdee63P29c+HTlixAglJCSoY8eOWrp0qfLy8uqcZszJyfE5VltzT0dKDZ+SrE9bn17xp1M85GoMcjWGP+V6JY2t2fW59dZb9fTTT+uzzz7T6dOnNXjwYIWFhTU5BgDtjc/N9oYNGzR79ux6TwP66rrrrlOHDh0kSf3791dBQYH3NKMkVVRUyO12+xyrzajTkQ1p69Mr/nSKh1yNQa7GMEOuVzol6Yvm1uykpCRJUkREhBYsWKDs7GzdddddslqtzYoBQHvjc+X76quvlJeX16wvW7ZsmS5cuKDKykplZGQoKiqqxmnGvLw89ezZ0+cYAKB+LVGzLwsLC9PYsWNrnK1sTgwA2hOfZ7YTEhK0bds2TZs2rcapwMacap0xY4YWL14sm82miRMnKjIyUqGhoUpMTNSFCxeUnp6uZcuWSZLPMQBAXS1RswEAzWfxeDweXzZ86KGH6n7YYtG6deuanYTD4VBGRoZiYmIUGhraqNiVnDlzptG5VN13h8/bBmx+vdH7b0lmONXtK3I1Brkawwy5NncZiZE120iNrdsN1ey2rs/NZYbfwZZ2NY5JYlz+pK3uRnLFme1PPvnEeweQ9evXt2xW3xASEuJ98EFjYwCAaq1VswEAvrvimu0///nPNV7v3bvXyFwAAM1AzQYA87lis117hcnLL79saDIAgKajZgOA+Vyx2b78mF8AgPlRswHAfK64Zru8vNz7pMf6XkvSzJkzjckMANAo1GwAMJ8rNtv//d//fcXXAADzoGYDgPlcsdm+8847WysPAEAzUbMBwHx4di4AAABgEJptAAAAwCA02wAAAIBBaLYBAAAAg9BsAwAAAAah2QYAAAAMQrMNAAAAGIRmGwAAADAIzTYAAABgEJptAAAAwCA02wAAAIBBaLYBAAAAg9BsAwAAAAah2QYAAAAMQrMNAAAAGIRmGwAAADCIzegvKC4u1urVq7VkyRK5XC6tWrVKpaWlmjBhgr7//e83KwYAAACYmaEz2w6HQ+vXr1dlZaUkac+ePYqOjtbSpUt18OBBlZeXNysGAAAAmJmhM9tWq1Vz587VypUrJUmZmZm6++67JUnDhg3TiRMnmhUbPnx4je9LSUlRSkqKJCk5OVnh4eGNzrmwEds2Zf8tyWaztXkOviJXY5CrMfwpVwCAuRnabAcHB9d4XVlZqbCwMElSSEiILl682KxYbXa7XXa73fu6qKjIkHG11v6/TXh4eJvn4CtyNQa5GsMMuUZGRrbp9wMAWkarXiAZFBQkp9MpSaqoqJDH42lWDAAAADCzVm22o6OjlZ2dLUnKzc1VREREs2IAAACAmRl+N5JvuvXWW/X000/rs88+0+nTpzV48GCFhYU1OQYAAACYWas020lJSZKkiIgILViwQNnZ2brrrrtktVqbFQMAAADMrFVntiUpLCxMY8eObbEYAAAAYFZMDwMAAAAGodkGAAAADEKzDQAAABiEZhsAAAAwCM02AAAAYJBWvxsJAMB/VFVV6eGHH1avXr0kSbNnz9aBAwd05MgRDRw4UHPmzJEk7dy506cYALQ3zGwDABqUl5enm2++WUlJSUpKSpLL5VJ2draWL1+ubt26KSMjQydPnvQpBgDtETPbAIAGHT9+XIcPH1ZmZqaioqIUGRmpUaNGyWKxKC4uTunp6QoODvYpFhsbW2f/KSkpSklJkSQlJycrPDy8UfkVNhBv7H7Mxmaz+f0YarsaxyQxLn/SVmOi2W6GqvvuqDcesPn1Vs4EAIwxcOBALVy4UN27d9e6devkdDoVGRkpSQoJCVFxcbGsVqt3mcmVYvWx2+2y2+3e10VFRS2Sd0vtp62Eh4f7/RhquxrHJDEuf2LkmC7XxfrQbAMAGtSvXz916NBBkhQdHa2qqio5nU5JUkVFhTwej4KCgnyKAUB7xJptAECDnn32WeXm5srtdistLU2VlZXKzs6WVL2eOyIiQtHR0T7FAKA9otkGADRoxowZWrdunebNm6chQ4Zo+vTpys3N1bZt27R7926NGzdOQ4cO9SkGAO0Ry0gAAA2KiorSqlWrasQWLlyow4cPa8qUKerZs2ejYgDQ3tBsAwAaJTAwUKNHj25SDADaG5aRAAAAAAah2QYAAAAMQrMNAAAAGIRmGwAAADAIzTYAAABgEJptAAAAwCA02wAAAIBBWvU+21VVVXr44YfVq1cvSdLs2bN14MABHTlyRAMHDtScOXMkSTt37vQpBgAAAJhZq85s5+Xl6eabb1ZSUpKSkpLkcrmUnZ2t5cuXq1u3bsrIyNDJkyd9igEAAABm16oz28ePH9fhw4eVmZmpqKgoRUZGatSoUbJYLIqLi1N6erqCg4N9isXGxrZm6gAAAECjtWqzPXDgQC1cuFDdu3fXunXr5HQ6FRkZKUkKCQlRcXGxrFard5nJlWL1SUlJUUpKiiQpOTlZ4eHhjc6xsCkDq6Up39sUNput1b6rucjVGORqDH/KFQBgbq3abPfr108dOnSQJEVHR6uqqkpOp1OSVFFRIY/Ho6CgIJ9i9bHb7bLb7d7XRUVFRg6nQa31veHh4W02xsYiV2OQqzHMkOvliQgAgH9r1TXbzz77rHJzc+V2u5WWlqbKykplZ2dLql7PHRERoejoaJ9iAAAAgNm1arM9Y8YMrVu3TvPmzdOQIUM0ffp05ebmatu2bdq9e7fGjRunoUOH+hQDAAAAzK5Vl5FERUVp1apVNWILFy7U4cOHNWXKFPXs2bNRMQAAAMDMWrXZrk9gYKBGjx7dpBgAAABgZjxBEgAAADAIzTYAAABgEJptAAAAwCA02wAAAIBBaLYBAAAAg9BsAwAAAAZp81v/XY2q7rujTixg8+ttkAkAAADaEjPbAAAAgEFotgEAAACD0GwDAAAABqHZBgAAAAxCsw0AAAAYhGYbAAAAMAjNNgAAAGAQ7rMNALjq8LwDAGbBzDYAAABgEGa2W0l9sywSMy0AAABXM2a2AQAAAIPQbAMAAAAGodkGAAAADMKa7TbGFfMAAABXL2a2AQAAAIP43cz2xo0bderUKcXHxyshIaGt0zEEdy4BcLUwU82mtgJoC37VbB88eFBut1vLli3Thg0bVFBQoGuuuaat02o1tQ8UhVfYloMHgLbmLzWbJhyAkSwej8fT1kn4auvWrRoxYoTi4+P18ccfy+l0asKECd73U1JSlJKSIklKTk5uqzQBAPr2mi1RtwFc/fxqzXZlZaXCwsIkSSEhIbp48WKN9+12u5KTk5tVsJ944olm5diayNUY5GoMcm1/vq1mS82v21fr39XVOK6rcUwS4/InbTUmv2q2g4KC5HQ6JUkVFRVyu91tnBEAoCHUbADws2Y7Ojpa2dnZkqS8vDz17NmzjTMCADSEmg0AUkBSUlJSWyfhq549e2r79u0qKCjQp59+qlmzZqlDhw4t/j3R0dEtvk+jkKsxyNUY5Nq+ULOb52oc19U4Jolx+ZO2GJNfXSApSQ6HQxkZGYqJiVFoaGhbpwMAuAJqNoD2zu+abQAAAMBf+NWabQAAAMCf+NWabaNt3LhRu3fvVnFxsWJiYto6HUlSWVmZnnnmGX344Yc6ePCgRo0apeeee65OnmbKvbi4WIsWLdLEiRPrzctMuf7pT3+S2+1WZGSkaXN1OBz63e9+p7feeksnT57UDTfcYMpci4uLtXz5ck2YMEEul0srV67UO++8I0kaMGCAz7HWzrWoqEgrV67Uhx9+qH//+9+64YYbVFVVZZpc0bC2/p1vLn+s777yp+NAY/jDMcNX/nJsaQyzHoeY2f6Pbz7prLCwUAUFBW2dkiQpNTVVU6dO1YIFCxQaGqqPP/64Tp5my/2FF16Q0+msNy8z5frZZ5+puLhYI0eONHWu+/bt07hx45ScnKzy8nK99tprpsvV4XBo/fr1qqyslCTt2bNH0dHRWrp0qQ4ePKjy8nKfY62d67vvvqs5c+YoMTFR586dU35+vmlyRcPa+ne+JfhjffeVvxwHGsNfjhm+8odjS2OY+ThEs/0fmZmZGjNmjCQpLi7Oe7uqtjZ58mTFxsZKkkpKSpSamlonTzPlfvToUXXs2FGhoaH15mWWXF0ul5577jlFREQoLS3N1Ll26dJFX3zxhUpLS3Xu3DmdPXvWdLlarVbNnTtXnTp1klT9/9PYsWMlScOGDdOJEyd8jrV2rj/+8Y917bXXSpK+/vprdenSxTS5omFt/TvfEvytvvvKX44DjeFPxwxf+cOxpTHMfByi2f4PX5501paOHTum0tJS9ejRo06eZsnd5XLpr3/9q+6++25J9f9MzZLrvn37dO2112ratGn6/PPP9c4775g216FDh+qrr3La5z8AABRKSURBVL7S22+/rT59+sjlcpku1+DgYAUHB3tf+/p33xZ51871sv3796tv374KCwszTa5o2NX09+EP9d1X/nQcaAx/Omb4yh+OLY1h5uMQzfZ/mPlJZw6HQ1u3btXPf/7zevM0S+67d+/WpEmT1LlzZ0n1/0zNkmtOTo7sdrtCQ0P1ve99TzExMabN9ZVXXtF9992nGTNmqE+fPvroo49Mm+tltfPxeDw+x9pCYWGh3njjDf30pz9tVP5oO2b7nW8qf6nvvvKn40Bj+NMxw1f+eGxpDDMdh2i2/8OsTzpzuVxavXq1Zs6cqYiIiHrzNEvu//rXv/TOO+8oKSlJubm5+sc//mHaXHv37q3CwkJJ0smTJ3X27FnT5lpaWqr8/Hy53W4dP35cP/jBD0yb62XfzCc3N7fO7+6VYq3N4XBo7dq1+vnPf+6dFTFrrvg/Zvudbwp/qu++8qfjQGP40zHDV/54bGkMMx2HuBvJf7TWk84aKyUlRampqSooKNAHH3yg/v37KyUlpUaeffr0MUXuEyZM0Pjx4zV+/Hilp6crKSmpTl5mybVv377629/+pj179uj48eN64okn9NJLL5ky1169eumPf/yj/vKXv6hLly76n//5H9P+XD/44AONHz9eEREReu6553TmzBnl5ubqzjvvVM+ePX2KWSyWVs11586d+uyzz/T555/rgw8+UM+ePRUTE2OqXFGXWWt2Y/hTffeVPx0HGsOfjhm+8qdjS2OY8TjEQ22+wV+edFZfnmbNnVyN4Q+5nj9/XtnZ2RoxYoR3xtjXmBn4U67tldl+51uCP/y/3VhX45ikq3NcV9uYzHIcotkGAAAADMKabQAAAMAgNNsAAACAQWi2YXpmWOlUXw5VVVWt8j3fpqSkpMXzAICWYIb63VJa6ziAqw/NNlrVxo0b9eWXXzbqMytXrtSePXsafP/ixYtKT09vdC7/+7//q08//dT7+qWXXtLf/va3erc9fvy4li5dWiOWlJSkkydP1tk2IyNDpaWlkqTPP/9cly5dkiQ98sgj3tsLffbZZ977en7TqlWr9K9//UsnTpzQ2rVrv3UMLpdLixcv1q5du664XVlZmXbv3u09WLhcrhr3S62qqvKr+6cCaH1G1G8jFRUV6bXXXmux/TXmOLBnzx45nU4tXrxY+fn5ev3111VWVqZNmzYpKyurxXKCf7C1dQJoP9LS0rRv3z5VVFTUua2O2+1WaGioZs+eXSP+j3/8Q6dOndKXX36pcePGKSQkpM5+L1y4oLVr1+rBBx9UVVWVXnnlFe+tiYqLi9WtWze5XC7dcsstmjZtmvdzY8aM0fr16zVy5EhdunRJH3zwgRITE+vNPT8/X9ddd533dWlpqUpKSjRgwIA6237wwQd64YUXlJSUpJdeeknDhg3TjBkzZLPZZLPZVFpaqmeeeUa//OUvFRsbq3/84x/enAsKCnT27FlZrVadP39eCxculMfj0fXXX6+77rqrzndt2bJFN9xwg44ePao+ffpo1KhRNd7Pzc3Vli1bJFU/pe7QoUMKCAjQoEGDdPz4cRUUFKh79+4KDAzUnDlzFB0dXe/4AbRvRtXvK9m2bZuuu+4676O0a3vooYeUmJionj176t5771Xfvn0lVT+katGiRcrIyJDL5ar3s++884727dsnq7X+OceKigrvfdAvj7cxx4Gqqirt2rVLAQEBqqio0Mcff6w77rhDR48erXEc+qalS5eqvLxcgYGBNeJOp1PBwcFasGBBvZ+D+dFso1UUFRXp+eef19KlSxUeHl7n/fpmVb/88ktt2rRJTz75pI4dO6ann35a8+fPV9euXWts179/f82dO1evvfaaFixYoNGjR3vfe+CBB7RixYo6+05OTta5c+fk8Xg0b948OZ1OlZWV6fe//706deqkJUuW1Nj2xIkTCgwMVFpamhISElRWVqaysjL94he/kFTd1L/wwguSpAcffFDPPPOMvvjiC917771atGiRpk2bJovFIovFopdfflnjxo1TbGysJCk2NtZ7O6VXXnnFm/+BAwd055136tixY8rJyanz89q+fbs8Ho9mzpypsrIyrVy5Unl5eZo+fbpstur/tSsqKtS7d2/FxcXpnnvu0eDBg7VhwwbNmjVLAQEBevLJJ7VgwQLv094AoDYj6/eV/OxnP/N5286dO2vu3Lm6dOmStm/fLqvVqn379snhcOjAgQPePJOSktSlSxdNnjxZkydP1qeffqrhw4crKChIR48eVWFhoW677Ta9+uqrKikp8TbajTkOOJ1Ode/eXRaLRaWlpcrKytKwYcOUlZWliooK9erVS5J06dKlGvesvly36xMQEODzzwLmQ7MNwxUXF2vZsmWaNWuWnn/+eTmdTrndbu+MgsfjUa9evfSrX/3K+5nPP/9cv//973XvvfeqsLBQAwcOVElJiX7729/qvvvu8zaql8XGxtaJXUlhYaGeeuopde7cWTt37lSPHj102223SZL3kd3f3HbNmjXq3LmzduzYofLycn344YdavHixIiMjJVUvEZGqi/nlJvayVatWqUOHDt6iPX369BozF5f3P3HiRJ0+fVr5+flyuVy6ePGiMjMzJanGPyDOnj2r5557Tp06ddLs2bNVXFwsqXqWZ9OmTXrkkUc0YcIE2e12RUdHKyQkRIsWLfLOijz44IPatWuX3nrrLZWWluoXv/iFBg8erCeeeMLnnx+A9qE16ndLsFgsOnLkiHJzcyVJ2dnZ6tGjh5YtW+bdZu7cuXVm5c+ePavf/OY3evjhh5Wfn+9dJvPVV19p4sSJ3u0acxxwuVzeB2WdOHFCffr0UUhIiP7+97/L4/HoiSeeUFFRkTp16qSVK1eqU6dOkqSBAwcqICCgzkNjLl26xNpwP0ezDcN169ZNDzzwgK677jq99tprSk5O1ooVKzRx4kTFx8frq6++0tatWyVV31h+9+7d2r9/vx555BHFxcVp06ZNGjRokGbMmKHevXvrd7/7nfr376/Zs2crLy9Pu3btksfj0a233qrp06f7lJPVatXixYtltVp14cIF2Ww2vfvuuw1u+01ZWVmyWCzeAivJW8APHTqkN954Qz/72c80aNAgvfbaa3rzzTcVGhoqq9WqP/7xj5KqH3u7Y8cOWa1WFRcXy+FwKC0tTcXFxcrKylJVVZWKi4uVlpYmqfoUbkhIiAIDA/X000/rxz/+sQ4cOKDnnntOBQUF6tixo3r06CG3260nn3xSf/vb31ReXq6uXbtqy5Yt6t69u55//nnl5ORo3rx5crvdGjVqlIYMGaLKykodPHiwcX+pANoFI+t3Tk6OMjMz9dBDD0mqXv9855136jvf+Y4kaf369frOd76j8ePHS6qezNiyZYvS0tI0fPjwGktELBaLAgICFBwcrHPnzuns2bP6wQ9+oOTkZO9Ewjf/kSBVL/m75ZZbNGDAADmdTjmdTu+s889//vMaP4fGHAcCAwPVq1cvnT9/XoGBgQoODlbnzp3173//W5MnT9aMGTO0Zs0aTZ06VZ06ddKhQ4f05ptvKjg4uMGnM1ZVVWnRokX66U9/ynI/P0SzDcNZLBZFR0erqqrKW4x++tOf6g9/+IPi4uJUWVmpzp07y+Vy6dKlSyovL9fKlSsVFhYmqbpwXS5048aN0/XXX689e/aoV69e6tevn2655Ra99957OnfunM85ud1uLVmyxKeZ7doGDRqk2267TRs3bvQW5MvjGj16tNxut95++2098sgjCggI0MSJE/XDH/6wxj7uuusu75iGDx+uZ555Rhs3btTEiRN1zz336NixY3r33Xf10EMP6dy5c1q7dq3cbrf69++vZ599VoGBgd4D0I4dO9S7d2/va6l6+YxUfUDo16+fpOq7lvTu3VvDhw/Xv//9bw0dOlSffPKJEhISdOjQIZ9/dgDaDyPrd+3lcd/mwIEDysnJ0bp163T48GF99NFH3vc8Ho9cLpd3lvjWW2/V6dOn1bdvX508edI7hm8u1XA4HHr88cd1//33a8SIEfroo48UFxfnUy5XOg6cP39eXbp00axZs/Tyyy/rhz/8odLS0lRVVeW9mLKoqEi9e/eWJN1000266aab9Mc//lEhISGy2WzeM5ahoaFyuVzeXOGfaLbRKpYuXapLly6psLBQCxcuVElJibp27aqkpCSVl5fr66+/VmJiou69917vLEdDunXrVu/Fgo1RVVWl5ORkBQQE6KuvvpLNZlNqamqD2y9atMg7C3333Xdr6NCheuGFF5Senq4RI0bU2Hbs2LG6/vrrJVUX33feeUf79++vsc3lonz27Fk9//zzysrKksvlktPp1MKFC+VyuVReXq4nnnhCFotFgwYN8s5mBAYGav78+d79XJ6Z37Nnj9xut5xOp9asWSNJiomJkc1m01//+lcNGDBAx44d06ZNm7xrxL/66it17969WT9LAFe31qrf33abwGPHjmn06NEKDAzU6NGja1xr4vF4dOHCBW9tc7vdev/99zV79mytX79es2fPVlVVlaxWqzwej6qqqjR16lR95zvfUVlZmSTpzJkzuv322737c7lcCggI8P5jwdfjgMPh0FtvvaWdO3fK4/FoxYoVstlseuqpp5SUlCSHw6Hy8vI6F4zm5OSoQ4cOstlsOn/+vCQpLCxMLperwQs94R9ottEqlixZooKCAr366qt65JFHtHDhQo0ZM0ZTpkxRRkaGjh49qpkzZzb7e6qqquotYrX94Q9/8P659sx2Q/lfXqt32dSpU7Vv3z7FxMQoKCjIG3e73Xr88ce1cuVKSdLkyZPrzGz/6Ec/kiSFh4dr/PjxGj9+vD799FM98MADOnr0qPLz8zVlyhQdOnRIaWlpuvfee2t8/re//a3++c9/6nvf+16Nme033nhDN954o3e7Q4cOafPmzQoJCVFlZaUkadiwYSooKJBUfUAJCgritn8AGtRa9ftyg9mQ2s34N9dfV1VV6cyZM4qJiVFRUZHy8vKUkZGhtWvX6vz580pLS/NeU1NSUqKnn366xpKNiooKnTlzRs8991yNfX7zLk2+Hgeio6O1ZMkSLVy4UMuXL9c///lPHT58WIGBgbrpppv0zDPPaPjw4XXGV1VVpbFjx6pTp07e2wPGxMSovLy8zoQN/AvNNlrN5dkQSZo/f75efPFFuVwuVVZWKjAwUC6X64pXY3+biooKJScna9SoUbLb7fVuk5+frxUrVtQosl9//bUCAgL0xhtvSKou6E6nUw888MAVTynedNNNGjlypEpLSxUcHOyNf/rppxowYIC6dOkiSXr33Xe9a69rs1qtGjlypPd+3x6PR6+99ppGjBih3NxcWa3WOhf0SNVF+fnnn9ewYcNqjP/111/XmDFjauR4+SCUkJCg9evXKyIiQqGhoTpx4oSuu+46ZWZmXvEfGgBgRP3u1KmTd/nf4cOHVVhYeMXtBw0apHfeeUf/9V//pfT0dDkcDu97y5cv16JFizRgwACNGTNGffr0UUREhPr3768vv/zSO8FgsVjUrVs3JScnez/rdru1atUqjR49WgMHDlRsbGyDtwSsraHjwIULFzRw4EAtX75cp0+f9k64jBo1Si+++KISEhJq7Mfj8eiee+7xPpfh8qx9jx49JKlF/jGDtkOzjVbjdDr12Wef1bjrxYIFC3Tx4kVJ1cW89n1aJd8euOJwOPT2229r1qxZstvtOnfunC5cuOCdzb0sKipK69evrxHbsWOHwsPDG2zQXS5XjdOHl0+BWiwWeTwepaeney+qcbvd+utf/+q9j6rH46mzZtvj8ejHP/5xje8YNGiQKisrtXbtWjkcDk2YMEFr167V6dOnNXHiRJWWltY4Zdq9e3dNnDhRH3zwgTf2/vvv69Zbb61zay6LxaL33ntP6enp+vLLL2W329W9e3elpaXp0Ucf1ebNm9WrVy+NHTvW5wMMgPbFiPo9YsQIvfnmm0pKSlLfvn01dOjQK+Zw88036+jRo3rwwQc1ePBg75IRSfrLX/6iyZMnKzIyUitWrNBTTz3lnZGOjIxs8JaDBQUF2rx5s/r06aNp06bpz3/+s1544QXdfffdio+P927XmOOAJPXu3Vtjx47Vzp079aMf/Uj5+fk6ePCgdu3apZ/85CfatGmTHnroIe+ESWFhoXbs2OG9U9XlWf7Tp097f46DBw+u0dDDf9Bso9Vcf/31NWYTpOqnbL3//vv6yU9+Uu9pNam6yHzbejW32625c+fqpptukiSdOHFC27Zt82nG1ul0XvG2SnfccYduueUWdejQQbm5ud5iePHiRW3ZskWDBw/WPffcI0k6deqUJHmLdO28KyoqtHjx4hrr+7Zu3ar3339f/fv3180336yHH35YNptNTz75pL744gu9+uqrevvttzVjxgxJ0qZNm7xPogwICFBZWZn3wQmdO3fWkSNH5HQ6tXbtWlmtVrlcLt12223eme20tDRlZGTo0UcfVc+ePTVv3jytWbNGpaWl3tl4APgmI+p3x44d6zyR8Ztqr/+2Wq117hIiVT+1t6KiQrfffrusVqvuuOMOnT171tuMv/3223rllVc0ZcoU72c++ugjffTRRzp37pxmzpyp7373u5KkOXPmKCcnRxs2bND+/fv18MMPS2rccaCyslLJycnq16+ffv3rXys0NFT79u3T3//+dz366KOKjIxUdHS0Xn31Vc2bN0+VlZXasGGDunTp4j2TeXlJyuX/ejweJScn67HHHlO3bt0a/JnBnCyeb7siATBQRkaGOnToUGM5xNWu9unWS5cuyWaz1btcxAgej0eXLl2q85QyAGgMM9Vvj8fTYA11u93eh4pddvLkSTmdzgZn010ul/Ly8jRw4EBD8kX7QrMNAAAAGIQFmgAAAIBBaLYBAAAAg9BsAwAAAAah2QYAAAAMQrMNAAAAGOT/AxEqlaTnWgoNAAAAAElFTkSuQmCC\n",
      "text/plain": [
       "<Figure size 864x288 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(12,4)) \n",
    "plt.subplot(121)\n",
    "plt.xlabel('每个订单的消费金额')\n",
    "df['order_amount'].plot(kind='hist',bins=50)  #bins:区间分数，影响柱子的宽度，值越大柱子越细。宽度=（列最大值-最小值）/bins\n",
    "#消费金额在100以内的订单占据了绝大多数\n",
    "\n",
    "plt.subplot(122)\n",
    "plt.xlabel('每个uid购买的数量')\n",
    "df.groupby(by='user_id')['order_products'].sum().plot(kind='hist',bins=50)\n",
    "#图二可知，每个用户购买数量非常小，集中在50以内\n",
    "# 两幅图得知，我们的用户主要是消费金额低，并且购买小于50的用户人数占据大多数（在电商领域是非常正常的现象）\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3.用户累计消费金额占比分析（用户的贡献度）"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>user_id</th>\n",
       "      <th>order_amount</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>10175</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>4559</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1948</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>925</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>10798</td>\n",
       "      <td>0.00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23565</th>\n",
       "      <td>7931</td>\n",
       "      <td>6497.18</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23566</th>\n",
       "      <td>19339</td>\n",
       "      <td>6552.70</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23567</th>\n",
       "      <td>7983</td>\n",
       "      <td>6973.07</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23568</th>\n",
       "      <td>14048</td>\n",
       "      <td>8976.33</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23569</th>\n",
       "      <td>7592</td>\n",
       "      <td>13990.93</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>23570 rows × 2 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "       user_id  order_amount\n",
       "0        10175          0.00\n",
       "1         4559          0.00\n",
       "2         1948          0.00\n",
       "3          925          0.00\n",
       "4        10798          0.00\n",
       "...        ...           ...\n",
       "23565     7931       6497.18\n",
       "23566    19339       6552.70\n",
       "23567     7983       6973.07\n",
       "23568    14048       8976.33\n",
       "23569     7592      13990.93\n",
       "\n",
       "[23570 rows x 2 columns]"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#进行用户分组，取出消费金额，进行求和，排序，重置索引\n",
    "user_cumsum = df.groupby(by='user_id')['order_amount'].sum().sort_values().reset_index()\n",
    "user_cumsum"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>user_id</th>\n",
       "      <th>order_amount</th>\n",
       "      <th>amount_cumsum</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>23565</th>\n",
       "      <td>7931</td>\n",
       "      <td>6497.18</td>\n",
       "      <td>2463822.60</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23566</th>\n",
       "      <td>19339</td>\n",
       "      <td>6552.70</td>\n",
       "      <td>2470375.30</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23567</th>\n",
       "      <td>7983</td>\n",
       "      <td>6973.07</td>\n",
       "      <td>2477348.37</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23568</th>\n",
       "      <td>14048</td>\n",
       "      <td>8976.33</td>\n",
       "      <td>2486324.70</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23569</th>\n",
       "      <td>7592</td>\n",
       "      <td>13990.93</td>\n",
       "      <td>2500315.63</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       user_id  order_amount  amount_cumsum\n",
       "23565     7931       6497.18     2463822.60\n",
       "23566    19339       6552.70     2470375.30\n",
       "23567     7983       6973.07     2477348.37\n",
       "23568    14048       8976.33     2486324.70\n",
       "23569     7592      13990.93     2500315.63"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#每个用户消费金额累加\n",
    "# 累加器举例：\n",
    "# a = [1,2,3,4,5,6,7]\n",
    "# print(np.cumsum(a))\n",
    "user_cumsum['amount_cumsum'] = user_cumsum['order_amount'].cumsum()\n",
    "user_cumsum.tail()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>user_id</th>\n",
       "      <th>order_amount</th>\n",
       "      <th>amount_cumsum</th>\n",
       "      <th>prop</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>23565</th>\n",
       "      <td>7931</td>\n",
       "      <td>6497.18</td>\n",
       "      <td>2463822.60</td>\n",
       "      <td>0.985405</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23566</th>\n",
       "      <td>19339</td>\n",
       "      <td>6552.70</td>\n",
       "      <td>2470375.30</td>\n",
       "      <td>0.988025</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23567</th>\n",
       "      <td>7983</td>\n",
       "      <td>6973.07</td>\n",
       "      <td>2477348.37</td>\n",
       "      <td>0.990814</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23568</th>\n",
       "      <td>14048</td>\n",
       "      <td>8976.33</td>\n",
       "      <td>2486324.70</td>\n",
       "      <td>0.994404</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23569</th>\n",
       "      <td>7592</td>\n",
       "      <td>13990.93</td>\n",
       "      <td>2500315.63</td>\n",
       "      <td>1.000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       user_id  order_amount  amount_cumsum      prop\n",
       "23565     7931       6497.18     2463822.60  0.985405\n",
       "23566    19339       6552.70     2470375.30  0.988025\n",
       "23567     7983       6973.07     2477348.37  0.990814\n",
       "23568    14048       8976.33     2486324.70  0.994404\n",
       "23569     7592      13990.93     2500315.63  1.000000"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "amount_total = user_cumsum['amount_cumsum'].max() #消费金额总值\n",
    "user_cumsum['prop'] = user_cumsum.apply(lambda x:x['amount_cumsum']/amount_total,axis=1)  #前xx名用户的总贡献率\n",
    "user_cumsum.tail()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x2a996aec988>"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "user_cumsum['prop'].plot()\n",
    "# 由图分析可知，前20000名用户贡献总金额的40%，剩余3500名用户贡献了60%。（2/8原则）"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 用户消费行为"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1.首购时间"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x2a996b76c88>"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#用户分组，取最小值，即为首购时间，\n",
    "# A  1997-1-1  \n",
    "# B  1997-1-1  \n",
    "# 1997-1-1   ?（2个）\n",
    "df.groupby(by='user_id')['order_date'].min().value_counts().plot()\n",
    "# 由图可知，首次购买的用户量在1月1号~2月10号呈明显上升趋势，后续开始逐步下降，猜测：有可能是公司产品的推广力度或者价格调整所致\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2.最后一次购买时间"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x2a996d63508>"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "df.groupby(by='user_id')['order_date'].max().value_counts().plot()\n",
    "# 大多数用户最后一次购买时间集中在前3个月，说明缺少忠诚用户。\n",
    "#  随着时间的推移，最后一次购买商品的用户量呈现上升趋势，猜测：这份数据选择是的前三个月消费的用户在后面18个月的跟踪记录"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 用户分层"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1.构建RFM模型"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>order_amount</th>\n",
       "      <th>order_date</th>\n",
       "      <th>order_products</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>user_id</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>11.77</td>\n",
       "      <td>1997-01-01</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>89.00</td>\n",
       "      <td>1997-01-12</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>156.46</td>\n",
       "      <td>1998-05-28</td>\n",
       "      <td>16</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>100.50</td>\n",
       "      <td>1997-12-12</td>\n",
       "      <td>7</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>385.61</td>\n",
       "      <td>1998-01-03</td>\n",
       "      <td>29</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "         order_amount order_date  order_products\n",
       "user_id                                         \n",
       "1               11.77 1997-01-01               1\n",
       "2               89.00 1997-01-12               6\n",
       "3              156.46 1998-05-28              16\n",
       "4              100.50 1997-12-12               7\n",
       "5              385.61 1998-01-03              29"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#透视表的使用（index:相当于groupby,values:取出的数据列，aggfunc:key值必须存在于values列中，并且必须跟随有效的聚合函数）\n",
    "rfm = df.pivot_table(index='user_id',\n",
    "                    values=['order_products','order_amount','order_date'],\n",
    "                    aggfunc={\n",
    "                        'order_date':'max',# 最后一次购买\n",
    "                        'order_products':'sum',# 购买产品的总数量\n",
    "                        'order_amount':'sum'  #消费总金额\n",
    "                        })\n",
    "rfm.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Timestamp('1998-06-30 00:00:00')"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "rfm['order_date'].max()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>M</th>\n",
       "      <th>order_date</th>\n",
       "      <th>F</th>\n",
       "      <th>R</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>user_id</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>11.77</td>\n",
       "      <td>1997-01-01</td>\n",
       "      <td>1</td>\n",
       "      <td>545.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>89.00</td>\n",
       "      <td>1997-01-12</td>\n",
       "      <td>6</td>\n",
       "      <td>534.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>156.46</td>\n",
       "      <td>1998-05-28</td>\n",
       "      <td>16</td>\n",
       "      <td>33.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>100.50</td>\n",
       "      <td>1997-12-12</td>\n",
       "      <td>7</td>\n",
       "      <td>200.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>385.61</td>\n",
       "      <td>1998-01-03</td>\n",
       "      <td>29</td>\n",
       "      <td>178.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "              M order_date   F      R\n",
       "user_id                              \n",
       "1         11.77 1997-01-01   1  545.0\n",
       "2         89.00 1997-01-12   6  534.0\n",
       "3        156.46 1998-05-28  16   33.0\n",
       "4        100.50 1997-12-12   7  200.0\n",
       "5        385.61 1998-01-03  29  178.0"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 用每个用户的最后一次购买时间-日期列中的最大值，最后再转换成天数，小数保留一位\n",
    "rfm['R'] = -(rfm['order_date']-rfm['order_date'].max())/np.timedelta64(1,'D')  #取相差的天数，保留一位小数\n",
    "rfm.rename(columns={'order_products':'F','order_amount':'M'},inplace=True)\n",
    "rfm.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>M</th>\n",
       "      <th>order_date</th>\n",
       "      <th>F</th>\n",
       "      <th>R</th>\n",
       "      <th>label</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>user_id</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>11.77</td>\n",
       "      <td>1997-01-01</td>\n",
       "      <td>1</td>\n",
       "      <td>545.0</td>\n",
       "      <td>一般发展客户</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>89.00</td>\n",
       "      <td>1997-01-12</td>\n",
       "      <td>6</td>\n",
       "      <td>534.0</td>\n",
       "      <td>一般发展客户</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>156.46</td>\n",
       "      <td>1998-05-28</td>\n",
       "      <td>16</td>\n",
       "      <td>33.0</td>\n",
       "      <td>重要保持客户</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>100.50</td>\n",
       "      <td>1997-12-12</td>\n",
       "      <td>7</td>\n",
       "      <td>200.0</td>\n",
       "      <td>一般挽留客户</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>385.61</td>\n",
       "      <td>1998-01-03</td>\n",
       "      <td>29</td>\n",
       "      <td>178.0</td>\n",
       "      <td>重要保持客户</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "              M order_date   F      R   label\n",
       "user_id                                      \n",
       "1         11.77 1997-01-01   1  545.0  一般发展客户\n",
       "2         89.00 1997-01-12   6  534.0  一般发展客户\n",
       "3        156.46 1998-05-28  16   33.0  重要保持客户\n",
       "4        100.50 1997-12-12   7  200.0  一般挽留客户\n",
       "5        385.61 1998-01-03  29  178.0  重要保持客户"
      ]
     },
     "execution_count": 19,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#RFM计算方式：每一列数据减去数据所在列的平均值，有正有负，根据结果值与1做比较，如果>=1,设置为1，否则0\n",
    "def rfm_func(x):  #x:分别代表每一列数据\n",
    "    level = x.apply(lambda x:'1' if x>=1 else '0')\n",
    "    label = level['R'] + level['F'] + level['M']  #举例：100    001\n",
    "    d = {\n",
    "        '111':'重要价值客户',\n",
    "        '011':'重要保持客户',\n",
    "        '101':'重要发展客户',\n",
    "        '001':'重要挽留客户',\n",
    "        '110':'一般价值客户',\n",
    "        '010':'一般保持客户',\n",
    "        '100':'一般发展客户',\n",
    "        '000':'一般挽留客户'\n",
    "        \n",
    "    }\n",
    "    result = d[label]\n",
    "    return result\n",
    "# rfm['R']-rfm['R'].mean()\n",
    "rfm['label'] = rfm[['R','F','M']].apply(lambda x:x-x.mean()).apply(rfm_func,axis =1)\n",
    "rfm.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0, 0.5, 'R')"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#客户分层可视化\n",
    "for label,grouped in rfm.groupby(by='label'):\n",
    "#     print(label,grouped)\n",
    "    x = grouped['F']  # 单个用户的购买数量\n",
    "    y = grouped['R']  #最近一次购买时间与98年7月的相差天数\n",
    "    plt.scatter(x,y,label=label)\n",
    "plt.legend()  #显示图例\n",
    "plt.xlabel('F')\n",
    "plt.ylabel('R')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 新老，活跃，回流用户分析"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "- 新用户的定义是第一次消费。\n",
    "- 活跃用户即老客，在某一个时间窗口内有过消费。\n",
    "- 不活跃用户则是时间窗口内没有消费过的老客。\n",
    "- 回流用户：相当于回头客的意思。\n",
    "- 用户回流的动作可以分为自主回流与人工回流，自主回流指玩家自己回流了，而人工回流则是人为参与导致的。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th>month</th>\n",
       "      <th>1997-01-01</th>\n",
       "      <th>1997-02-01</th>\n",
       "      <th>1997-03-01</th>\n",
       "      <th>1997-04-01</th>\n",
       "      <th>1997-05-01</th>\n",
       "      <th>1997-06-01</th>\n",
       "      <th>1997-07-01</th>\n",
       "      <th>1997-08-01</th>\n",
       "      <th>1997-09-01</th>\n",
       "      <th>1997-10-01</th>\n",
       "      <th>1997-11-01</th>\n",
       "      <th>1997-12-01</th>\n",
       "      <th>1998-01-01</th>\n",
       "      <th>1998-02-01</th>\n",
       "      <th>1998-03-01</th>\n",
       "      <th>1998-04-01</th>\n",
       "      <th>1998-05-01</th>\n",
       "      <th>1998-06-01</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>user_id</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>2.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>2.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "month    1997-01-01  1997-02-01  1997-03-01  1997-04-01  1997-05-01  \\\n",
       "user_id                                                               \n",
       "1               1.0         0.0         0.0         0.0         0.0   \n",
       "2               2.0         0.0         0.0         0.0         0.0   \n",
       "3               1.0         0.0         1.0         1.0         0.0   \n",
       "4               2.0         0.0         0.0         0.0         0.0   \n",
       "5               2.0         1.0         0.0         1.0         1.0   \n",
       "\n",
       "month    1997-06-01  1997-07-01  1997-08-01  1997-09-01  1997-10-01  \\\n",
       "user_id                                                               \n",
       "1               0.0         0.0         0.0         0.0         0.0   \n",
       "2               0.0         0.0         0.0         0.0         0.0   \n",
       "3               0.0         0.0         0.0         0.0         0.0   \n",
       "4               0.0         0.0         1.0         0.0         0.0   \n",
       "5               1.0         1.0         0.0         1.0         0.0   \n",
       "\n",
       "month    1997-11-01  1997-12-01  1998-01-01  1998-02-01  1998-03-01  \\\n",
       "user_id                                                               \n",
       "1               0.0         0.0         0.0         0.0         0.0   \n",
       "2               0.0         0.0         0.0         0.0         0.0   \n",
       "3               2.0         0.0         0.0         0.0         0.0   \n",
       "4               0.0         1.0         0.0         0.0         0.0   \n",
       "5               0.0         2.0         1.0         0.0         0.0   \n",
       "\n",
       "month    1998-04-01  1998-05-01  1998-06-01  \n",
       "user_id                                      \n",
       "1               0.0         0.0         0.0  \n",
       "2               0.0         0.0         0.0  \n",
       "3               0.0         1.0         0.0  \n",
       "4               0.0         0.0         0.0  \n",
       "5               0.0         0.0         0.0  "
      ]
     },
     "execution_count": 21,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "pivoted_counts = df.pivot_table(\n",
    "                index='user_id',\n",
    "                columns ='month',\n",
    "                values = 'order_dt',\n",
    "                aggfunc = 'count'\n",
    ").fillna(0)\n",
    "pivoted_counts.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th>month</th>\n",
       "      <th>1997-01-01</th>\n",
       "      <th>1997-02-01</th>\n",
       "      <th>1997-03-01</th>\n",
       "      <th>1997-04-01</th>\n",
       "      <th>1997-05-01</th>\n",
       "      <th>1997-06-01</th>\n",
       "      <th>1997-07-01</th>\n",
       "      <th>1997-08-01</th>\n",
       "      <th>1997-09-01</th>\n",
       "      <th>1997-10-01</th>\n",
       "      <th>1997-11-01</th>\n",
       "      <th>1997-12-01</th>\n",
       "      <th>1998-01-01</th>\n",
       "      <th>1998-02-01</th>\n",
       "      <th>1998-03-01</th>\n",
       "      <th>1998-04-01</th>\n",
       "      <th>1998-05-01</th>\n",
       "      <th>1998-06-01</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>user_id</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "month    1997-01-01  1997-02-01  1997-03-01  1997-04-01  1997-05-01  \\\n",
       "user_id                                                               \n",
       "1                 1           0           0           0           0   \n",
       "2                 1           0           0           0           0   \n",
       "3                 1           0           1           1           0   \n",
       "4                 1           0           0           0           0   \n",
       "5                 1           1           0           1           1   \n",
       "\n",
       "month    1997-06-01  1997-07-01  1997-08-01  1997-09-01  1997-10-01  \\\n",
       "user_id                                                               \n",
       "1                 0           0           0           0           0   \n",
       "2                 0           0           0           0           0   \n",
       "3                 0           0           0           0           0   \n",
       "4                 0           0           1           0           0   \n",
       "5                 1           1           0           1           0   \n",
       "\n",
       "month    1997-11-01  1997-12-01  1998-01-01  1998-02-01  1998-03-01  \\\n",
       "user_id                                                               \n",
       "1                 0           0           0           0           0   \n",
       "2                 0           0           0           0           0   \n",
       "3                 1           0           0           0           0   \n",
       "4                 0           1           0           0           0   \n",
       "5                 0           1           1           0           0   \n",
       "\n",
       "month    1998-04-01  1998-05-01  1998-06-01  \n",
       "user_id                                      \n",
       "1                 0           0           0  \n",
       "2                 0           0           0  \n",
       "3                 0           1           0  \n",
       "4                 0           0           0  \n",
       "5                 0           0           0  "
      ]
     },
     "execution_count": 22,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# 由于浮点数不直观，并且需要转成是否消费过即可，用0、1表示\n",
    "df_purchase = pivoted_counts.applymap(lambda x:1 if x>0 else 0)\n",
    "# apply:作用与dataframe数据中的一行或者一列数据\n",
    "# applymap:作用与dataframe数据中的每一个元素\n",
    "# map:本身是一个series的函数，在df结构中无法使用map函数，map函数作用于series中每一个元素的\n",
    "df_purchase.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th>month</th>\n",
       "      <th>1997-01-01</th>\n",
       "      <th>1997-02-01</th>\n",
       "      <th>1997-03-01</th>\n",
       "      <th>1997-04-01</th>\n",
       "      <th>1997-05-01</th>\n",
       "      <th>1997-06-01</th>\n",
       "      <th>1997-07-01</th>\n",
       "      <th>1997-08-01</th>\n",
       "      <th>1997-09-01</th>\n",
       "      <th>1997-10-01</th>\n",
       "      <th>1997-11-01</th>\n",
       "      <th>1997-12-01</th>\n",
       "      <th>1998-01-01</th>\n",
       "      <th>1998-02-01</th>\n",
       "      <th>1998-03-01</th>\n",
       "      <th>1998-04-01</th>\n",
       "      <th>1998-05-01</th>\n",
       "      <th>1998-06-01</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>user_id</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>new</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>new</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>new</td>\n",
       "      <td>unactive</td>\n",
       "      <td>return</td>\n",
       "      <td>active</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>return</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>return</td>\n",
       "      <td>unactive</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>new</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>return</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>return</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>new</td>\n",
       "      <td>active</td>\n",
       "      <td>unactive</td>\n",
       "      <td>return</td>\n",
       "      <td>active</td>\n",
       "      <td>active</td>\n",
       "      <td>active</td>\n",
       "      <td>unactive</td>\n",
       "      <td>return</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>return</td>\n",
       "      <td>active</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "      <td>unactive</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "month   1997-01-01 1997-02-01 1997-03-01 1997-04-01 1997-05-01 1997-06-01  \\\n",
       "user_id                                                                     \n",
       "1              new   unactive   unactive   unactive   unactive   unactive   \n",
       "2              new   unactive   unactive   unactive   unactive   unactive   \n",
       "3              new   unactive     return     active   unactive   unactive   \n",
       "4              new   unactive   unactive   unactive   unactive   unactive   \n",
       "5              new     active   unactive     return     active     active   \n",
       "\n",
       "month   1997-07-01 1997-08-01 1997-09-01 1997-10-01 1997-11-01 1997-12-01  \\\n",
       "user_id                                                                     \n",
       "1         unactive   unactive   unactive   unactive   unactive   unactive   \n",
       "2         unactive   unactive   unactive   unactive   unactive   unactive   \n",
       "3         unactive   unactive   unactive   unactive     return   unactive   \n",
       "4         unactive     return   unactive   unactive   unactive     return   \n",
       "5           active   unactive     return   unactive   unactive     return   \n",
       "\n",
       "month   1998-01-01 1998-02-01 1998-03-01 1998-04-01 1998-05-01 1998-06-01  \n",
       "user_id                                                                    \n",
       "1         unactive   unactive   unactive   unactive   unactive   unactive  \n",
       "2         unactive   unactive   unactive   unactive   unactive   unactive  \n",
       "3         unactive   unactive   unactive   unactive     return   unactive  \n",
       "4         unactive   unactive   unactive   unactive   unactive   unactive  \n",
       "5           active   unactive   unactive   unactive   unactive   unactive  "
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def active_status(data): #data：每一行数据（共18列）\n",
    "    status = [] #存储用户18个月的状态（new|active|unactive|return|unreg）\n",
    "    for i in range(18):\n",
    "        #判断本月没有消费==0\n",
    "        if data[i] ==0:\n",
    "            if len(status)==0: #前几个月没有任何记录（也就是97年1月==0）\n",
    "                status.append('unreg')  \n",
    "            else:#之前的月份有记录（判断上一个月状态）\n",
    "                if status[i-1] =='unreg':#一直没有消费过\n",
    "                    status.append('unreg')\n",
    "                else:#上个月的状态可能是：new|active|unative|reuturn\n",
    "                    status.append('unactive')\n",
    "        else:#本月有消费==1\n",
    "            if len(status)==0:\n",
    "                status.append('new') #第一次消费\n",
    "            else:#之前的月份有记录（判断上一个月状态）\n",
    "                if status[i-1]=='unactive':\n",
    "                    status.append('return') #前几个月不活跃，现在又回来消费了，回流用户\n",
    "                elif  status[i-1]=='unreg':\n",
    "                    status.append('new') #第一次消费\n",
    "                else:#new|active\n",
    "                    status.append('active') #活跃用户\n",
    "            \n",
    "    return pd.Series(status,df_purchase.columns) #值：status,列名：18个月份\n",
    "\n",
    "purchase_states = df_purchase.apply(active_status,axis=1) #得到用户分层结果\n",
    "purchase_states.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th>month</th>\n",
       "      <th>1997-01-01</th>\n",
       "      <th>1997-02-01</th>\n",
       "      <th>1997-03-01</th>\n",
       "      <th>1997-04-01</th>\n",
       "      <th>1997-05-01</th>\n",
       "      <th>1997-06-01</th>\n",
       "      <th>1997-07-01</th>\n",
       "      <th>1997-08-01</th>\n",
       "      <th>1997-09-01</th>\n",
       "      <th>1997-10-01</th>\n",
       "      <th>1997-11-01</th>\n",
       "      <th>1997-12-01</th>\n",
       "      <th>1998-01-01</th>\n",
       "      <th>1998-02-01</th>\n",
       "      <th>1998-03-01</th>\n",
       "      <th>1998-04-01</th>\n",
       "      <th>1998-05-01</th>\n",
       "      <th>1998-06-01</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>active</th>\n",
       "      <td>NaN</td>\n",
       "      <td>1157.0</td>\n",
       "      <td>1681</td>\n",
       "      <td>1773.0</td>\n",
       "      <td>852.0</td>\n",
       "      <td>747.0</td>\n",
       "      <td>746.0</td>\n",
       "      <td>604.0</td>\n",
       "      <td>528.0</td>\n",
       "      <td>532.0</td>\n",
       "      <td>624.0</td>\n",
       "      <td>632.0</td>\n",
       "      <td>512.0</td>\n",
       "      <td>472.0</td>\n",
       "      <td>571.0</td>\n",
       "      <td>518.0</td>\n",
       "      <td>459.0</td>\n",
       "      <td>446.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>new</th>\n",
       "      <td>7846.0</td>\n",
       "      <td>8476.0</td>\n",
       "      <td>7248</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>return</th>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>595</td>\n",
       "      <td>1049.0</td>\n",
       "      <td>1362.0</td>\n",
       "      <td>1592.0</td>\n",
       "      <td>1434.0</td>\n",
       "      <td>1168.0</td>\n",
       "      <td>1211.0</td>\n",
       "      <td>1307.0</td>\n",
       "      <td>1404.0</td>\n",
       "      <td>1232.0</td>\n",
       "      <td>1025.0</td>\n",
       "      <td>1079.0</td>\n",
       "      <td>1489.0</td>\n",
       "      <td>919.0</td>\n",
       "      <td>1029.0</td>\n",
       "      <td>1060.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>unactive</th>\n",
       "      <td>NaN</td>\n",
       "      <td>6689.0</td>\n",
       "      <td>14046</td>\n",
       "      <td>20748.0</td>\n",
       "      <td>21356.0</td>\n",
       "      <td>21231.0</td>\n",
       "      <td>21390.0</td>\n",
       "      <td>21798.0</td>\n",
       "      <td>21831.0</td>\n",
       "      <td>21731.0</td>\n",
       "      <td>21542.0</td>\n",
       "      <td>21706.0</td>\n",
       "      <td>22033.0</td>\n",
       "      <td>22019.0</td>\n",
       "      <td>21510.0</td>\n",
       "      <td>22133.0</td>\n",
       "      <td>22082.0</td>\n",
       "      <td>22064.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "month     1997-01-01  1997-02-01  1997-03-01  1997-04-01  1997-05-01  \\\n",
       "active           NaN      1157.0        1681      1773.0       852.0   \n",
       "new           7846.0      8476.0        7248         NaN         NaN   \n",
       "return           NaN         NaN         595      1049.0      1362.0   \n",
       "unactive         NaN      6689.0       14046     20748.0     21356.0   \n",
       "\n",
       "month     1997-06-01  1997-07-01  1997-08-01  1997-09-01  1997-10-01  \\\n",
       "active         747.0       746.0       604.0       528.0       532.0   \n",
       "new              NaN         NaN         NaN         NaN         NaN   \n",
       "return        1592.0      1434.0      1168.0      1211.0      1307.0   \n",
       "unactive     21231.0     21390.0     21798.0     21831.0     21731.0   \n",
       "\n",
       "month     1997-11-01  1997-12-01  1998-01-01  1998-02-01  1998-03-01  \\\n",
       "active         624.0       632.0       512.0       472.0       571.0   \n",
       "new              NaN         NaN         NaN         NaN         NaN   \n",
       "return        1404.0      1232.0      1025.0      1079.0      1489.0   \n",
       "unactive     21542.0     21706.0     22033.0     22019.0     21510.0   \n",
       "\n",
       "month     1998-04-01  1998-05-01  1998-06-01  \n",
       "active         518.0       459.0       446.0  \n",
       "new              NaN         NaN         NaN  \n",
       "return         919.0      1029.0      1060.0  \n",
       "unactive     22133.0     22082.0     22064.0  "
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#把unreg状态用nan替换\n",
    "purchase_states_ct = purchase_states.replace('unreg',np.NaN).apply(lambda x:pd.value_counts(x))\n",
    "purchase_states_ct.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x2a996ec8648>"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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mQvMja5hWzK6urqUyWQURbyZAAAAcHENGZj7+/t14sQJeV5DvnwAAIAZ9dRTT+nJJ5/U5z73OX3mM59Rb2+vHnvsMX3uc5/TE088IUn6sz/7M506dUqbN29Wb2+vHn300YSrnryGTIz5fF6SWAobAABghhw+fFjbt2/XPffcox07dmjjxo3avn27+vr61NXVpTVr1ui1117TjTfeqF/96le67rrrki550hquh9k5p3w+r2w2S2AGAACYIffff78kaeXKlXriiSe0bt06vfHGGxoYGFBvb6+uu+46/eQnP9EnPvEJ/eQnP9Gf/MmfJFzx5DXcCPOJEyd05syZpMsAAABYUHK5XO3+I488ogcffFDPPPOMPv/5z2vlypW69tprtXPnTn30ox9lhHm+y+fzMsYwugwAABasFU1+oscLgkCvvfaaduzYoebmZm3dulVLlizRqlWrtGbNGi1evFirV6+e0Rpnk3HOuaSLmMjRo0dn7FjWWj333HNyzqlQKMzYcQEAAJJ0xx13aM2aNUmXUTeOHDmiV199ddy+bdu2XfT5DdWSceTIEQ0PD8tam3QpAAAAqBMNFZi7urrk+75KpVLSpQAAAKBONExgDsNQ+/fvVzqdTroUAAAA1JGGCczd3d0ql8us7AcAAIApaZhZMvL5vIIgULlcTroUAACAWXVwr69CYebGRXM5q6uua9xBx4YIzKVSSQcPHlQmk1EYhkmXAwAAMKsKBU+DZ2a6kWBmAvPIisvXXnvtjBxvLjRES8b+/ftlrSUsAwAAJCyfz9dCc71oiBHmrq4upVIpVSqVpEsBAABYkB5++GHdcMMN2rdvn773ve+pUCjoq1/9qk6dOqWrr75aX/7yl/UP//APeuWVVyRJL774op5++mk99dRTuuWWW3TLLbdox44dkqRPfvKT5x3vqaeeUhiG+u1vf6uhoSE9+eSTWrp06Zy8tgU/wjw0NKTDhw8rCBri3AAAACARHR0d+tCHPqTvfe97kqTnn39eGzdu1Pbt29XX16euri49+uijeuihh/TQQw/p6aefntLxJOnw4cPavn277rnnHu3cuXNWX89YCz5FdnV1SRIX+wEAAMyijRs36t57761tHzp0SG+//bbeeOMNDQwMqLe3V5s2bZrwGKVSSZlM5oLHk6T7779fkrRy5co57RxY8IE5n88rk8mwWAkAAMAsampqGre9fv163XjjjfrjP/5j/eIXv9DKlSslSZlMRmfOnJEkOeeUSqXU398vSXrttdd09913X/B4kpTL5WbzJVzUgg7M/f39OnHihLLZbNKlAAAAzJlcziZ+vAceeEBbtmzRjh071NzcrK1bt0qSbr/9dn3xi1/USy+9pEceeUR33XWXnnjiCf36179WW1vbjNY9U4xzziVdxESOHj067e99/fXX9frrr8sYo3n+MgEAAKbtjjvu0Jo1a5Iuo24cOXJEr7766rh927Ztu+jzF+xFf8455fN5ZbNZwjIAAACmbcEG5hMnTuj06dNJlwEAAIA6t2ADcz6flzFGxWIx6VIAAABQxxZkYLbWat++fVzsBwAAgMu2IGfJeP/99zU0NERgBgAADWnnzp0aGBiYseO1trbq1ltvnbHj1ZsFGZjz+bw8z6MdAwAANKSRhULqVT6flyRde+214/Z/+9vf1mOPPTbn9Sy4lowwDLV///7aKjEAAACoL/l8vhaax0oiLEsLcIS5u7tb5XJZ6XQ66VIAAAAawlNPPaVbbrlFt9xyi3bs2KGnn35af/iHf6jf/va3Ghoa0pNPPqmmpiY99thjKhQKWrt2rb7+9a+rVCrpa1/7mk6cOKGWlhZ961vf0rPPPqtXXnlFkvTiiy/q6aefrv2chx9+WM8884wk6dlnn9XGjRt1991367nnntPatWt155136qtf/apOnTqlq6++Wl/+8pdn5PUtuBHmfD6vIAhULpeTLgUAAKBhHT58WNu3b9c999yjnTt3qq+vT5/5zGf01FNP6dixYzp58qSef/55bdq0Sc8995zuvfdeHThwQI8++qgeeughPfTQQ+PC8rnuu+++2uIjb775pu688049//zz2rhxo7Zv366+vj51dXXNyGtZUCPMpVJJ3d3dSqfTCsMw6XIAAAAaTqlUkiTdf//9kqSVK1eqUqkoCAK98MIL2rFjh86cOVPLbffcc48k6ZOf/OSUfs769et14sQJDQ4OqrW1VblcTocOHdLbb7+tN954o9bHvWnTpst+TQtqhPnAgQOKokiVSiXpUgAAABpGKpVSf3+/JOm1116TJOVyuXHPeeGFF3Tvvfdq69attceuvPJK7dmzR5K0fft2/ehHP5IkZTKZ2uQNE63YfOONN+oHP/iB7rrrLklxiH7wwQf1zDPP6POf/7xWrlw5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\n",
      "text/plain": [
       "<Figure size 864x432 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#数据可视化，面积图\n",
    "purchase_states_ct.fillna(0).T.plot.area(figsize=(12,6))  #填充nan之后，进行行列变换\n",
    "#由图可知：灰色区域是不活跃用户，占比较大\n",
    "#前三个月新用户，还是活跃用户呈现了上升趋势，猜测由于活动造成的影响\n",
    "#3月份过后，紫色回流用户，红色活跃用户，都呈现下降趋势，并且趋于平稳状态\n",
    "#3月份过后，新用户量几乎没有大量增加"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x2a998cce3c8>"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 864x432 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#每月中回流用户占比情况（占所有用户的比例）\n",
    "plt.figure(figsize=(12,6))\n",
    "rate = purchase_states_ct.fillna(0).T.apply(lambda x:x/x.sum(),axis=1)\n",
    "plt.plot(rate['return'],label='return')\n",
    "plt.plot(rate['active'],label='active')\n",
    "plt.legend()\n",
    "# 由图可知，前3个月，活跃用户占比比较大，维持在7%左右，而回流用户比例在上升，由于new用户还没有足够时间变成回流用户\n",
    "# 4月份过后，不论是活跃用户，还是回流用户都呈现出下降趋势，但是回流用户依然高于活跃用户。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 用户的购买周期"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>a</th>\n",
       "      <th>b</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>NaN</td>\n",
       "      <td>0.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>NaN</td>\n",
       "      <td>2.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>NaN</td>\n",
       "      <td>3.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>NaN</td>\n",
       "      <td>4.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>NaN</td>\n",
       "      <td>5.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    a    b\n",
       "0 NaN  0.0\n",
       "1 NaN  1.0\n",
       "2 NaN  2.0\n",
       "3 NaN  3.0\n",
       "4 NaN  4.0\n",
       "5 NaN  5.0"
      ]
     },
     "execution_count": 27,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#shift函数：将数据移动到一定的位置\n",
    "data1 = pd.DataFrame({\n",
    "    'a':[0,1,2,3,4,5],\n",
    "    'b':[5,4,3,2,1,0]\n",
    "})\n",
    "data1.shift(axis=0) #整体向下移动一个位置（默认值：axis=0）\n",
    "data1.shift(axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "count                      46089\n",
       "mean     68 days 23:22:13.567662\n",
       "std      91 days 00:47:33.924168\n",
       "min              0 days 00:00:00\n",
       "25%             10 days 00:00:00\n",
       "50%             31 days 00:00:00\n",
       "75%             89 days 00:00:00\n",
       "max            533 days 00:00:00\n",
       "Name: order_date, dtype: object"
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#计算购买周期（购买日期的时间差值）\n",
    "order_diff = df.groupby(by='user_id').apply(lambda x:x['order_date']-x['order_date'].shift()) #当前订单日期-上一次订单日期\n",
    "order_diff.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x2a998cb9348>"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "(order_diff/np.timedelta64(1,'D')).hist(bins = 20) #影响柱子的宽度，  每个柱子的宽度=（最大值-最小值）/bins\n",
    "# 得知：平均消费周期为68天\n",
    "# 大多数用户消费周期低于100天\n",
    "# 呈现典型的长尾分布，只有小部分用户消费周期在200天以上（不积极消费的用户），可以在这批用户消费后3天左右进行电话回访后者短信\n",
    "# 赠送优惠券等活动，增大消费频率\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 用户生命周期"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x2a996ea5d08>"
      ]
     },
     "execution_count": 30,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#计算方式：用户最后一次购买日期(max)-第一次购买的日期(min)。如果差值==0，说明用户仅仅购买了一次\n",
    "user_life = df.groupby('user_id')['order_date'].agg(['min','max'])\n",
    "(user_life['max']==user_life['min']).value_counts().plot.pie(autopct='%1.1f%%') #格式化成1为小数\n",
    "plt.legend(['仅消费一次','多次消费'])\n",
    "#一半以上的用户仅仅消费了一次，说明运营不利，留存率不好"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "count                       23570\n",
       "mean     134 days 20:55:36.987696\n",
       "std      180 days 13:46:43.039788\n",
       "min               0 days 00:00:00\n",
       "25%               0 days 00:00:00\n",
       "50%               0 days 00:00:00\n",
       "75%             294 days 00:00:00\n",
       "max             544 days 00:00:00\n",
       "dtype: object"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "(user_life['max']-user_life['min']).describe()  #生命周期分析\n",
    "#用户平均生命周期为134天，但是中位数==0，再次验证大多数用户消费了一次，低质量用户。\n",
    "# 75%分位数以后的用户，生命周期>294天，属于核心用户，需要着重维持。\n",
    "# 前三个月的新用户数据，所以分析的是这些用户的生命周期"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 绘制所有用户生命周期直方图+多次消费"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0, 0.5, '用户人数')"
      ]
     },
     "execution_count": 32,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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88+bRo0amT179liDLN27dzf//Oc/rcd79+41mZmZXscz5uhny5lnnmmef/55q+w///mPcTqdZsKECR5nf8usXLnSDBw40GzevNmEhISY8PBwExQUZMLDw01YWJhZuHChSUtLM1FRUdY2JSUlZufOnUaSNegyadIkc+utt5r8/HwzevRor7Dt6z0qM27cOPPAAw9U+Lwxxjz88MNVGnQ59rPnmmuuscL23r17TYsWLUyjRo2sQZcOHTqYgwcP+vy8qy8cJzoNBacGh8OhmTNnqlWrVho0aJCKi4tVWFioF198Ue+8845KSkpUVFQkY4wefvhhPf7445KkvXv36sYbb1RYWJgSExOVmJjosd9Dhw5p0KBBevXVVz3KjTH65JNPdMYZZ0iSrr32WvXv39+aH5aenq4zzzzTZz39FRISIunovGW3262dO3fqtNNOs56Pjo7Wm2++qYSEBJ/bf/fdd7riiis0ceJEvfnmm0pLS9Ovv/5qPV9aWqqoqChdeumlWr16tZ5//nlFRERYz7vdboWEhCg/P18hISHWRUdl5YWFhXK73T6P3apVK6Wmpko6OteyjDFGEydO1JgxYyp8j/Ly8rR+/Xqdc845Xs/deuutXsc8dt562YWxx84ZP1ZwcLDPee5PPfWUbrrpJkVFRekvf/mLmjRpolGjRumKK67wuR+gPsjMzFRGRoa+++47hYWFqX///vr66681fvx43X777erWrZsWLFjgtd2jjz6qdevW6ZlnntHtt9+u1atXKy0tTbGxsdZrVq1apbFjx6pHjx6SpP/5n//Rxx9/rEWLFln96l//+lclJydLkjVnd9WqVZKkyMhIjzng//u//6uRI0fq7rvvVv/+/fXQQw9p0KBBuvrqqzV+/Hj169dPkhQUFGRtExoaqvz8fGvecnp6urp27aqdO3cqKSlJf/zxh3UdzwsvvKDPP//co50hISG6/fbbrX5z7969kqS1a9ce970NDQ3V1q1brbaWl5GRoTZt2ljXu7jdbv3zn/+U2+1Wp06drNfl5eXp0Ucf1ZQpUyQd7QNbtmypbdu2Wa9JS0vTrFmztGHDBo0YMULff/+9Ro8ebT1/9dVX6+eff1bbtm114403auTIkbrwwgslHe0zg4ODde655+rgwYNq2LCh2rdvr/Xr16tNmzaS5DUX3+FwKDIyUpLUvXt3SVJ2drau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7du3T7169bJGa1q3bu3xGl8jC8YY3XfffYqIiFCDBg3UoEEDvfbaazpw4IDCwsJ0/vnn+zUHOiEhwecXgJycnApHth988EF16dLFOlV5rLKLjco79r04cuSICgsLdffdd6uoqEgPPvigrrzySut5VqVDfXTgwAFdcsklKiws1LRp03TxxRdb87YvuOACTZ482VoUpswLL7ygJk2a6L777rPKlixZoksvvVSHDh3Sq6++6vOL8+HDh7VmzRpNmDDBKhs9erTXwiRlF3eXKbs4cM2aNVbZF198oZtvvllpaWlWmKvq3/Ddd9+tvXv3qrS0VPn5+R6hMjMzUwUFBRVOVajM999/r5iYmApDn3R0lN/XoEv5wC95Drr4mossHe2bV69erYyMDKWkpOiiiy7yeD43N1eHDx/2Cvc//vijNWresGFDffvtt9bZibJrpMp77rnnVFBQoJkzZ1oDNk899ZQeeeQRSUdHlx977DHrjEJFqjOyXVJSomeffdbji16Zffv2yRjj9VlWplu3bpKkefPm6bbbbtPkyZP166+/Kjw8XL169apw2mR9QNiG3njjDY/R58LCQk2cONGjwy4pKTnu3Lhjlc3X+vnnnxUfH2+V5+bmatmyZdZV0WVcLpd1dfOHH36opUuXqm3bth6vWbdunT7//HOtWLGiSu0rKiqy5guWH50oP5+xbA5go0aNrLKnn35akZGRioqKsi4K+u9//yvp6PSXvLw8r/0++eSTGjhwoCIjIxUZGen1ReLQoUPKycnR5s2bPULx1KlTtWvXLm3cuFEhISFq3Lix3njjDS1dulTPPPOM3nnnHUlHR4TefPNNq6MuLS31mGuYlJRU6ci2y+WyLlgyxmjcuHHasGGDdeeCstds3LhR2dnZmjFjhs477zyv/R17RXpERITmzZunuXPnat26ddZol6/XAvWF0+nUq6++qq5du1oDGi+99JIGDx6sPn366LffftP69eutEJiWlqbHHntMH330kTVy+sMPP2jGjBnasGGDiouLrZVkyw9aLF26VB07dlTXrl0lHQ2Izz77bKUj28cquw6kpKREiYmJGjp0qLKzs/Xvf/9b0dHRfl0rc6zWrVtbK1Hm5uZ6BOv3339ff/nLXzzCbUUDLuX717feekuXX355lepyogoKCtSjRw/de++9ev311z0+N3788Uf16dNHN910kzWKLR09m5mcnKyXX37Z2kefPn2s/wd79uypMPROmDBBW7Zs0WOPPSaHw6GNGzcqJSVFCQkJatiwofr27XvcOt95550+R+kPHTpU4XU006ZNU2lpqc//HxkZGYqKivIaSS+fDQoKCvTII48oMzNTt99+u2666Sbrd1hvB11q906DCDQ5OTmmd+/eJicnxypLTEw0F198sXXvZWOMeeWVV8z555/vcx/33XefueOOO7zK27Zta9q3b++xwtb333/vtfiBMca8++675ptvvjHGGPPll1+a8ePHm59++sl6fu/evSYmJsb8v//3/6rcxoULF5rQ0FDTpEkTj/ts+/oJCwszf/vb3467z5UrV5pLL73U53MlJSXmhhtuMGvWrKlw+y+//NIEBQWZli1betz3Oicnx2MVzzJr1qwxDz/8sMcxevbsaZ566iljjDFJSUkmJCTEWtHzeD8NGza02rl06VLTvn17n/dp7dGjh2nfvr258847TUZGhtfz8fHxpkGDBqZhw4aV/jgcDjNw4MAK3w+gPigqKjIbN240o0aNMk2bNjUPPPCAOXjwoPW82+02vXr1su6HbYwxb775pmnatKnHQixvvvmmCQ0NNbNmzbLWE9i5c6dp2rSpmTVrlvW6fv36ea1/kJaWZp588kkTGxvrVb/ffvvNLF++3HTv3t20b9/e7N6926xZs8ace+65plGjRua+++4zqamp1uv37dtnJFl/52X32i7P7Xab3r17m1WrVhljjvZfZ511lnnllVc8Xnf//febUaNGGWOO9pG33XabCQ0N9Vh195dffjEOh6PShWR8KS4uNocOHTLFxcUei96cf/755oUXXvAoKyws9FprICsry+zbt88Yc3TthpycHPPzzz+bdu3aGWOMx+dlmYceesh06tSpwjrl5+eb7du3m7fffts0a9bMKn/xxRfNmWeeabKzs62yPXv2mDFjxpjo6Gjz7LPPGmOOrtK5bNkyI8ns3r3blJaWWms6XHTRRWb16tU+jztp0iTz8MMPG5fL5bEg29NPP22ioqLM5s2bPV7/2Wefmffee8/85S9/MZdcconX/i677DKPRW3KfPHFFx6rnm7YsKHS9+NURtiGl5KSErN///4T3o/L5aqB2vyfpKSkChdbCTSVLYFbpqbfnxPhawVMf+zcudPjgxDA//nmm2/M6NGjzc0332x6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\n",
      "text/plain": [
       "<Figure size 864x432 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(12,6))\n",
    "plt.subplot(121)\n",
    "((user_life['max']-user_life['min'])/np.timedelta64(1,'D')).hist(bins=15)\n",
    "plt.title('所有用户生命周期直方图')\n",
    "plt.xlabel('生命周期天数')\n",
    "plt.ylabel('用户人数')\n",
    "\n",
    "plt.subplot(122)\n",
    "u_1 = (user_life['max']-user_life['min']).reset_index()[0]/np.timedelta64(1,'D')\n",
    "u_1[u_1>0].hist(bins=15)\n",
    "plt.title('多次消费的用户生命周期直方图')\n",
    "plt.xlabel('生命周期天数')\n",
    "plt.ylabel('用户人数')\n",
    "# 对比可知，第二幅图过滤掉了生命周期==0的用户，呈现双峰结构\n",
    "# 虽然二图中还有一部分用户的生命周期趋于0天，但是比第一幅图好了很多，虽然进行了多次消费，但是不成长期\n",
    "# 来消费，属于普通用户，可针对性进行营销推广活动\n",
    "# 少部分用户生命周期集中在300~500天，属于我们的忠诚客户，需要大力度维护此类客户"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 复购率和回购率分析"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 复购率分析"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x2a99c75d488>"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 864x432 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#计算方式：在自然月内，购买多次的用户在总消费人数中的占比（若客户在同一天消费了多次，也称之复购用户）\n",
    "#消费者有三种：消费记录>=2次的；消费中人数；本月无消费用户；\n",
    "#复购用户:1    非复购的消费用户：0   自然月没有消费记录的用户：NAN(不参与count计数)\n",
    "purchase_r = pivoted_counts.applymap(lambda x: 1 if x>1 else np.NaN  if x==0 else 0)\n",
    "purchase_r.head()\n",
    "#purchase_r.sum() :求出复购用户\n",
    "#purchase_r.count():求出所有参与购物的用户（NAN不参与计数）\n",
    "(purchase_r.sum()/purchase_r.count()).plot(figsize=(12,6))\n",
    "# 前三个月复购率开始上升，后续趋于平稳维持在20%~22%之间。\n",
    "# 分析前三个月复购率低的原因，可能是因为大批新用户仅仅购买一次造成的。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 回购率分析"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th>month</th>\n",
       "      <th>1997-01-01</th>\n",
       "      <th>1997-02-01</th>\n",
       "      <th>1997-03-01</th>\n",
       "      <th>1997-04-01</th>\n",
       "      <th>1997-05-01</th>\n",
       "      <th>1997-06-01</th>\n",
       "      <th>1997-07-01</th>\n",
       "      <th>1997-08-01</th>\n",
       "      <th>1997-09-01</th>\n",
       "      <th>1997-10-01</th>\n",
       "      <th>1997-11-01</th>\n",
       "      <th>1997-12-01</th>\n",
       "      <th>1998-01-01</th>\n",
       "      <th>1998-02-01</th>\n",
       "      <th>1998-03-01</th>\n",
       "      <th>1998-04-01</th>\n",
       "      <th>1998-05-01</th>\n",
       "      <th>1998-06-01</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>user_id</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>1.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "month    1997-01-01  1997-02-01  1997-03-01  1997-04-01  1997-05-01  \\\n",
       "user_id                                                               \n",
       "1               0.0         NaN         NaN         NaN         NaN   \n",
       "2               0.0         NaN         NaN         NaN         NaN   \n",
       "3               0.0         NaN         1.0         0.0         NaN   \n",
       "4               0.0         NaN         NaN         NaN         NaN   \n",
       "5               1.0         0.0         NaN         1.0         1.0   \n",
       "\n",
       "month    1997-06-01  1997-07-01  1997-08-01  1997-09-01  1997-10-01  \\\n",
       "user_id                                                               \n",
       "1               NaN         NaN         NaN         NaN         NaN   \n",
       "2               NaN         NaN         NaN         NaN         NaN   \n",
       "3               NaN         NaN         NaN         NaN         NaN   \n",
       "4               NaN         NaN         0.0         NaN         NaN   \n",
       "5               1.0         0.0         NaN         0.0         NaN   \n",
       "\n",
       "month    1997-11-01  1997-12-01  1998-01-01  1998-02-01  1998-03-01  \\\n",
       "user_id                                                               \n",
       "1               NaN         NaN         NaN         NaN         NaN   \n",
       "2               NaN         NaN         NaN         NaN         NaN   \n",
       "3               0.0         NaN         NaN         NaN         NaN   \n",
       "4               NaN         0.0         NaN         NaN         NaN   \n",
       "5               NaN         1.0         0.0         NaN         NaN   \n",
       "\n",
       "month    1998-04-01  1998-05-01  1998-06-01  \n",
       "user_id                                      \n",
       "1               NaN         NaN         NaN  \n",
       "2               NaN         NaN         NaN  \n",
       "3               NaN         0.0         NaN  \n",
       "4               NaN         NaN         NaN  \n",
       "5               NaN         NaN         NaN  "
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#计算方式：在一个时间窗口内进行了消费，在下一个窗口内又进行了消费\n",
    "def purchase_back(data):\n",
    "    status = [] #存储用户回购率状态\n",
    "    #1:回购用户   0：非回购用户（当前月消费了，下个未消费）   NaN:当前月份未消费\n",
    "    for i in range(17):\n",
    "        #当前月份消费了\n",
    "        if data[i] == 1:\n",
    "            if data[i+1]==1:\n",
    "                status.append(1) #回购用户\n",
    "            elif data[i+1] == 0: #下个月未消费\n",
    "                status.append(0)\n",
    "        else: #当前月份未进行消费\n",
    "            status.append(np.NaN)\n",
    "    status.append(np.NaN) #填充最后一列数据\n",
    "    return pd.Series(status,df_purchase.columns)\n",
    "\n",
    "purchase_b = df_purchase.apply(purchase_back,axis=1)\n",
    "purchase_b.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x2a99bf13d08>"
      ]
     },
     "execution_count": 49,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1440x288 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#回购率可视化\n",
    "plt.figure(figsize=(20,4))\n",
    "plt.subplot(211)\n",
    "#回购率\n",
    "(purchase_b.sum() / purchase_b.count()).plot(label='回购率')\n",
    "#复购率\n",
    "(purchase_r.sum()/purchase_r.count()).plot(label='复购率')\n",
    "plt.legend()\n",
    "plt.ylabel('百分比%')\n",
    "plt.title('用户回购率和复购率对比图')\n",
    "#回购率可知，平稳后在30%左右，波形性稍微较大\n",
    "#复购率低于回购率，平稳后在20%左右，波动小较小\n",
    "#前三个月不困是回购还是复购，都呈现上升趋势，说明新用户需要一定时间来变成复购或者回购用户\n",
    "#结合新老用户分析，新客户忠诚度远低于老客户忠诚度。\n",
    "\n",
    "#回购人数与购物总人数\n",
    "plt.subplot(212)\n",
    "plt.plot(purchase_b.sum(),label='回购人数')\n",
    "plt.plot(purchase_b.count(),label='购物总人数')\n",
    "plt.xlabel('month')\n",
    "plt.ylabel('人数')\n",
    "plt.legend()\n",
    "# 前三个月购物总人数远远大于回购人数，主要是因为很多新用户在1月份进了首次购买\n",
    "# 三个月后，回购人数和购物总数开始稳定，回购人数稳定在1000左右，购物总人数在2000左右。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
