import { Layout } from "@consta/uikit/Layout";
import { Text } from "@consta/uikit/Text";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <Layout
      flex={1}
      className="Footer"
      verticalAlign="bottom"
      style={{
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Link to="/" style={{ textDecoration: "none", marginTop: "40px" }}>
        <Text size="sm">Сделано командой - «Простите, у нас вдохновение»</Text>
      </Link>
    </Layout>
  );
};

export default Footer;
