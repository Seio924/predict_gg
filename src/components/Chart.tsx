import React from "react";
import ApexCharts from "react-apexcharts";
import { useRecoilValue } from "recoil";
import styled from "styled-components";
import { winningRateState } from "../atom";

const ChartContainer = styled.div`
  width: 840px;
`;

function Chart() {
  const winningRate = useRecoilValue(winningRateState);

  const changeToTime = (num: number) => {
    let minute = 0;
    let second = 0;
    if (num != 0) {
      minute = parseInt(`${num / 60}`);
      second = num % 60;
    }
    const time =
      String(minute).padStart(2, "0") + ":" + String(second).padStart(2, "0");
    return time;
  };

  return (
    <>
      <ChartContainer>
        <ApexCharts
          type="area"
          height="200"
          series={[
            {
              name: "winning rate blue",
              data: winningRate?.map((rate) => ({
                x: rate[0], // x값에 해당하는 데이터 필드를 적절히 지정해야 합니다.
                y: rate[1] < 50 ? 0 : rate[1] - 50, // y값에 해당하는 데이터 필드를 적절히 지정해야 합니다.
              })),
            },
            {
              name: "winning rate red",
              data: winningRate?.map((rate) => ({
                x: rate[0], // x값에 해당하는 데이터 필드를 적절히 지정해야 합니다.
                y: rate[2] < 50 ? 0 : 50 - rate[2], // y값에 해당하는 데이터 필드를 적절히 지정해야 합니다.
              })),
            },
          ]}
          options={{
            plotOptions: {
              area: {
                fillTo: "origin",
              },
            },
            colors: ["#5E82E1", "#D64E5B"],
            theme: {
              mode: "dark",
            },
            chart: {
              type: "area",
              background: "transparent",
              toolbar: {
                show: false,
              },
            },
            legend: {
              position: "top",
              horizontalAlign: "center",
              offsetY: 20,
            },
            markers: {
              shape: "rect",
            },

            dataLabels: {
              enabled: false,
            },
            stroke: {
              colors: ["#D64E5B", "#5E82E1"],
              width: 0,
              curve: "smooth",
            },
            title: {
              text: "",
              align: "left",
              style: {
                fontSize: "14px",
              },
            },
            xaxis: {
              labels: {
                show: false, // x-axis 라벨 숨기기
              },
              tooltip: {
                enabled: false,
              },
              type: "category",
              axisBorder: {
                show: false,
              },
              axisTicks: {
                show: false,
              },
            },
            yaxis: {
              show: false,
              tickAmount: 1,
              floating: false,
              min: -50,
              max: 50,
              forceNiceScale: false,
              labels: {
                style: {
                  colors: "#8e8da4",
                },
                offsetY: -7,
                offsetX: 0,
                formatter: function (value) {
                  console.log(value);
                  return Math.abs(value).toString();
                },
              },
              axisBorder: {
                show: false,
              },
              axisTicks: {
                show: false,
              },
            },

            fill: { type: "solid", opacity: 0.5 },

            tooltip: {
              x: {},
              custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                const yValue =
                  Math.abs(
                    w.globals.initialSeries[seriesIndex].data[dataPointIndex].y
                  ) + 50;
                const xValue = changeToTime(
                  w.globals.initialSeries[seriesIndex].data[dataPointIndex].x
                );
                if (yValue !== 50) {
                  return (
                    "<div style='background-color: rgba(26, 27, 29, 0.9); color: #eeeeef; padding: 10px; font-size: 12px; font-family: PretendardMedium;'>" +
                    xValue +
                    "&nbsp;&nbsp;&nbsp;" +
                    yValue +
                    "%" +
                    "</div>"
                  );
                } else {
                  return "";
                }
              },
            },
            grid: {
              yaxis: {
                lines: {
                  show: false,
                  offsetX: -30,
                },
              },
            },
          }}
        />
      </ChartContainer>
    </>
  );
}

export default Chart;
