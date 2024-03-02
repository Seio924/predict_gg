import styled, { css } from "styled-components";

const defaultBackgroundColor = css`
  background-color: rgba(0, 0, 0, 0);
  border: 1px solid #ffffff;
`;

const firstColorBackground = css`
  background-image: linear-gradient(
    265deg,
    rgba(24, 200, 255, 0.7),
    rgba(147, 63, 254, 0.7)
  );
`;

const secondColorBackground = css`
  background-image: linear-gradient(
    265deg,
    rgba(198, 197, 197, 0.7),
    rgba(91, 90, 90, 0.7)
  );
`;

const Btn = styled.div<IProps>`
  display: flex;
  justify-content: center;
  align-items: center;
  height: ${(props) => props.height || "45px"};
  width: 100%;
  border-radius: 7px;
  margin: ${(props) => props.margin || "0"}; /* Margin 설정 */
  cursor: pointer;
  ${(props) =>
    props.btnColor === true
      ? firstColorBackground
      : props.btnColor === false
      ? secondColorBackground
      : defaultBackgroundColor};
`;

const BtnText = styled.p<IProps>`
  font-size: ${(props) => props.textSize || "20px"};
  font-family: ${(props) => props.textFont || "PretendardBold, sans-serif"};
  color: #eeeeef;
`;

interface IProps {
  btnColor?: boolean;
  onClick?: () => void;
  height?: string;
  textSize?: string;
  textFont?: string;
  margin?: string; // margin props 추가
  children?: React.ReactNode;
}

function Button({
  btnColor,
  onClick,
  height,
  textSize,
  textFont,
  margin, // margin props 추가
  children,
}: IProps) {
  return (
    <>
      <Btn
        height={height}
        btnColor={btnColor}
        onClick={onClick}
        margin={margin}
      >
        <BtnText textSize={textSize} textFont={textFont}>
          {children}
        </BtnText>
      </Btn>
    </>
  );
}

export default Button;
