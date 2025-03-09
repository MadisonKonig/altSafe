import React from "react";
import Navbar from "./shared/Navbar";
import Button from "./shared/Button";
import styles from "./shared/styles";
const Home = () => {
  return (
    <>
      <Navbar />
      <Button color={styles.btnPrimary} label="Get Started" />
      <Button color={styles.btnSecondary} label="Get Started" />
    </>
  );
};

export default Home;
