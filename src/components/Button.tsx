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

const Btn = styled.div<{ btnColor?: boolean; height?: string }>`
  display: flex;
  justify-content: center;
  align-items: center;
  height: ${(props) => props.height || "45px"};
  width: 100%;
  border-radius: 7px;
  margin-top: 15px;
  cursor: pointer;
  ${(props) =>
    props.btnColor === true
      ? firstColorBackground
      : props.btnColor === false
      ? secondColorBackground
      : defaultBackgroundColor};
  &:first-child {
    margin-right: 18px;
  }
`;

const BtnText = styled.p<IProps>`
  font-size: ${(props) => props.textSize || "14px"};
  font-weight: ${(props) => props.textWeight || "400"};
  color: #eeeeef;
`;

interface IProps {
  btnColor?: boolean;
  onClick?: () => void;
  height?: string;
  textSize?: string;
  textWeight?: string;
  children?: React.ReactNode;
}

function Button({
  btnColor,
  onClick,
  height,
  textSize,
  textWeight,
  children,
}: IProps) {
  return (
    <>
      <Btn height={height} btnColor={btnColor} onClick={onClick}>
        <BtnText textSize={textSize} textWeight={textWeight}>
          {children}
        </BtnText>
      </Btn>
    </>
  );
}

export default Button;
