import { Layout } from "@consta/uikit/Layout";
import { Text } from "@consta/uikit/Text";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <Layout flex={1} className="header">
      <Text view="primary" size="m" lineHeight="m">
        <Link to="/" style={{ textDecoration: "none" }}>
          <Text size="2xl">SeedVideo</Text>
        </Link>
      </Text>
    </Layout>
  );
};

export default Header;
