import { Grid } from "@consta/uikit/Grid";
import PropTypes from "prop-types";

const Container = ({ children }) => {
  return (
    <Grid
      cols={1}
      xAlign="center"
      yAlign="top"
      gap="xl"
      style={{ marginTop: "30px" }}
      breakpoints={{
        768: {
          cols: 3,
        },
      }}
    >
      {children}
    </Grid>
  );
};
Container.propTypes = {
  children: PropTypes.node.isRequired,
};
export default Container;
